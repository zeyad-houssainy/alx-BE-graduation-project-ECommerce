from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count
from .models import Category
from .serializers import CategorySerializer, CategoryDetailSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Category model providing full CRUD operations.
    
    Available actions:
    - GET /api/categories/ - List all categories
    - POST /api/categories/ - Create a new category
    - GET /api/categories/{slug}/ - Retrieve a specific category
    - PUT /api/categories/{slug}/ - Update a category (full update)
    - PATCH /api/categories/{slug}/ - Update a category (partial update)
    - DELETE /api/categories/{slug}/ - Delete a category
    - GET /api/categories/{slug}/products/ - Get products in a category
    - GET /api/categories/featured/ - Get featured categories
    - GET /api/categories/popular/ - Get popular categories
    - POST /api/categories/bulk-update/ - Bulk update categories
    - DELETE /api/categories/bulk-delete/ - Bulk delete categories
    """
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at', 'updated_at']
    ordering = ['name']
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CategoryDetailSerializer
        return CategorySerializer

    def get_queryset(self):
        queryset = Category.objects.all()
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(is_active=True)
        return queryset

    def perform_create(self, serializer):
        """Create a new category"""
        serializer.save()

    def perform_update(self, serializer):
        """Update a category"""
        serializer.save()

    def perform_destroy(self, instance):
        """Soft delete a category by setting is_active to False"""
        instance.is_active = False
        instance.save()

    @action(detail=True, methods=['get'])
    def products(self, request, slug=None):
        """Get all products in a specific category"""
        try:
            category = self.get_object()
            products = category.products.filter(is_active=True)
            
            # Apply pagination
            page = self.paginate_queryset(products)
            if page is not None:
                from products.serializers import ProductListSerializer
                serializer = ProductListSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            from products.serializers import ProductListSerializer
            serializer = ProductListSerializer(products, many=True)
            return Response(serializer.data)
        except Category.DoesNotExist:
            return Response(
                {'error': 'Category not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured categories"""
        featured_categories = self.get_queryset().filter(is_active=True)[:6]
        serializer = self.get_serializer(featured_categories, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def popular(self, request):
        """Get popular categories based on product count"""
        popular_categories = self.get_queryset().annotate(
            product_count=Count('products')
        ).filter(
            product_count__gt=0,
            is_active=True
        ).order_by('-product_count')[:10]
        
        serializer = self.get_serializer(popular_categories, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search categories by name or description"""
        query = request.query_params.get('q', '')
        if not query:
            return Response(
                {'error': 'Search query parameter "q" is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.get_queryset().filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def bulk_update(self, request):
        """Bulk update categories"""
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        category_ids = request.data.get('category_ids', [])
        update_data = request.data.get('update_data', {})
        
        if not category_ids:
            return Response(
                {'error': 'category_ids field is required'}, 
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
        update_data.pop('created_at', None)
        update_data.pop('updated_at', None)
        
        updated_count = 0
        allowed_fields = ['name', 'description', 'is_active']
        
        for category_id in category_ids:
            try:
                category = Category.objects.get(id=category_id)
                for field, value in update_data.items():
                    if field in allowed_fields and hasattr(category, field):
                        # Validate field type before setting
                        field_obj = category._meta.get_field(field)
                        if hasattr(field_obj, 'validate'):
                            field_obj.validate(value, category)
                        setattr(category, field, value)
                category.save()
                updated_count += 1
            except Category.DoesNotExist:
                continue
            except Exception as e:
                # Log validation errors but continue with other categories
                continue
        
        return Response({
            'message': f'Successfully updated {updated_count} categories',
            'updated_count': updated_count
        })

    @action(detail=False, methods=['delete'])
    def bulk_delete(self, request):
        """Bulk delete categories (soft delete)"""
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        category_ids = request.data.get('category_ids', [])
        
        if not category_ids:
            return Response(
                {'error': 'category_ids field is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        deleted_count = 0
        for category_id in category_ids:
            try:
                category = Category.objects.get(id=category_id)
                category.is_active = False
                category.save()
                deleted_count += 1
            except Category.DoesNotExist:
                continue
        
        return Response({
            'message': f'Successfully deleted {deleted_count} categories',
            'deleted_count': deleted_count
        })

    @action(detail=True, methods=['post'])
    def toggle_active(self, request, slug=None):
        """Toggle category active status"""
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        category = self.get_object()
        category.is_active = not category.is_active
        category.save()
        
        serializer = self.get_serializer(category)
        return Response({
            'message': f'Category {"activated" if category.is_active else "deactivated"} successfully',
            'category': serializer.data
        })

    @action(detail=True, methods=['get'])
    def stats(self, request, slug=None):
        """Get category statistics"""
        category = self.get_object()
        total_products = category.products.count()
        active_products = category.products.filter(is_active=True).count()
        out_of_stock = category.products.filter(stock_quantity=0, is_active=True).count()
        
        return Response({
            'category': self.get_serializer(category).data,
            'stats': {
                'total_products': total_products,
                'active_products': active_products,
                'out_of_stock': out_of_stock,
                'in_stock': active_products - out_of_stock
            }
        })
