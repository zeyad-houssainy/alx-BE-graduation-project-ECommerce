from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import Product
from .serializers import (
    ProductSerializer, ProductDetailSerializer, ProductCreateUpdateSerializer
)
from .filters import ProductFilter


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Product model providing full CRUD operations.
    
    Available actions:
    - GET /api/products/ - List all products
    - POST /api/products/ - Create a new product
    - GET /api/products/{slug}/ - Retrieve a specific product
    - PUT /api/products/{slug}/ - Update a product (full update)
    - PATCH /api/products/{slug}/ - Update a product (partial update)
    - DELETE /api/products/{slug}/ - Delete a product
    - GET /api/products/search/ - Search products
    - GET /api/products/featured/ - Get featured products
    - GET /api/products/out-of-stock/ - Get out of stock products
    - POST /api/products/bulk-update/ - Bulk update products
    - DELETE /api/products/bulk-delete/ - Bulk delete products
    """
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description', 'category__name']
    ordering_fields = ['name', 'price', 'created_at', 'updated_at', 'stock_quantity']
    ordering = ['-created_at']
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ProductCreateUpdateSerializer
        return ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.select_related('category', 'created_by')
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(is_active=True)
        return queryset

    def perform_create(self, serializer):
        """Create a new product and set the creator"""
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        """Update a product"""
        serializer.save()

    def perform_destroy(self, instance):
        """Soft delete a product by setting is_active to False"""
        instance.is_active = False
        instance.save()

    @action(detail=False, methods=['get'])
    def search(self, request):
        """Advanced search functionality"""
        query = request.query_params.get('q', '')
        if not query:
            return Response(
                {'error': 'Search query parameter "q" is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.get_queryset().filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured products (first 6 active products)"""
        featured_products = self.get_queryset()[:6]
        serializer = self.get_serializer(featured_products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def out_of_stock(self, request):
        """Get products that are out of stock"""
        out_of_stock_products = self.get_queryset().filter(stock_quantity=0)
        serializer = self.get_serializer(out_of_stock_products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        """Get products with low stock (less than 10 items)"""
        low_stock_products = self.get_queryset().filter(
            stock_quantity__lt=10, 
            stock_quantity__gt=0
        )
        serializer = self.get_serializer(low_stock_products, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def update_stock(self, request, slug=None):
        """Update product stock quantity"""
        product = self.get_object()
        new_stock = request.data.get('stock_quantity')
        
        if new_stock is None:
            return Response(
                {'error': 'stock_quantity field is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            new_stock = int(new_stock)
            if new_stock < 0:
                return Response(
                    {'error': 'Stock quantity cannot be negative'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        except (ValueError, TypeError):
            return Response(
                {'error': 'Invalid stock quantity value'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        product.stock_quantity = new_stock
        product.save()
        
        serializer = self.get_serializer(product)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def bulk_update(self, request):
        """Bulk update products"""
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        product_ids = request.data.get('product_ids', [])
        update_data = request.data.get('update_data', {})
        
        if not product_ids:
            return Response(
                {'error': 'product_ids field is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not update_data:
            return Response(
                {'error': 'update_data field is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Remove fields that shouldn't be updated
        update_data.pop('id', None)
        update_data.pop('slug', None)
        update_data.pop('created_by', None)
        update_data.pop('created_at', None)
        update_data.pop('updated_at', None)
        
        updated_count = 0
        allowed_fields = ['name', 'description', 'price', 'category', 'stock_quantity', 'is_active']
        
        for product_id in product_ids:
            try:
                product = Product.objects.get(id=product_id)
                for field, value in update_data.items():
                    if field in allowed_fields and hasattr(product, field):
                        # Validate field type before setting
                        field_obj = product._meta.get_field(field)
                        if hasattr(field_obj, 'validate'):
                            field_obj.validate(value, product)
                        setattr(product, field, value)
                product.save()
                updated_count += 1
            except Product.DoesNotExist:
                continue
            except Exception as e:
                # Log validation errors but continue with other products
                continue
        
        return Response({
            'message': f'Successfully updated {updated_count} products',
            'updated_count': updated_count
        })

    @action(detail=False, methods=['delete'])
    def bulk_delete(self, request):
        """Bulk delete products (soft delete)"""
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        product_ids = request.data.get('product_ids', [])
        
        if not product_ids:
            return Response(
                {'error': 'product_ids field is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        deleted_count = 0
        for product_id in product_ids:
            try:
                product = Product.objects.get(id=product_id)
                product.is_active = False
                product.save()
                deleted_count += 1
            except Product.DoesNotExist:
                continue
        
        return Response({
            'message': f'Successfully deleted {deleted_count} products',
            'deleted_count': deleted_count
        })

    @action(detail=True, methods=['post'])
    def toggle_active(self, request, slug=None):
        """Toggle product active status"""
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        product = self.get_object()
        product.is_active = not product.is_active
        product.save()
        
        serializer = self.get_serializer(product)
        return Response({
            'message': f'Product {"activated" if product.is_active else "deactivated"} successfully',
            'product': serializer.data
        })
