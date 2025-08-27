from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Q
from .models import UserProfile
from .serializers import (
    UserSerializer, UserProfileSerializer, UserCreateSerializer,
    UserLoginSerializer
)


class UserRegistrationView(APIView):
    """Separate view for user registration"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        """User registration endpoint"""
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                user = serializer.save()
                # Profile is created automatically by signal
                
                # Generate tokens
                refresh = RefreshToken.for_user(user)
                return Response({
                    'message': 'User registered successfully',
                    'user': UserSerializer(user).data,
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    """Separate view for user login"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        """User login endpoint"""
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'message': 'Login successful',
                    'user': UserSerializer(user).data,
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': 'Invalid credentials'
                }, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for User model providing full CRUD operations.
    
    Available actions:
    - GET /api/users/ - List all users (admin only)
    - POST /api/users/ - Create a new user
    - GET /api/users/{id}/ - Retrieve a specific user
    - PUT /api/users/{id}/ - Update a user (full update)
    - PATCH /api/users/{id}/ - Update a user (partial update)
    - DELETE /api/users/{id}/ - Delete a user
    - GET /api/users/profile/ - Get current user's profile
    - PUT /api/users/update_profile/ - Update current user's profile
    - GET /api/users/search/ - Search users

    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['username', 'date_joined']
    ordering = ['username']
    
    def get_permissions(self):
        if self.action in ['create', 'register', 'login']:
            return [AllowAny()]
        elif self.action in ['list']:
            return [IsAdminUser()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    def get_queryset(self):
        """Filter queryset based on user permissions"""
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)

    @action(detail=False, methods=['get'])
    def profile(self, request):
        """Get current user's profile"""
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    @action(detail=False, methods=['put', 'patch'])
    def update_profile(self, request):
        """Update current user's profile"""
        user = request.user
        if hasattr(user, 'profile'):
            serializer = UserProfileSerializer(user.profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search users by username, email, or name"""
        query = request.query_params.get('q', '')
        if not query:
            return Response(
                {'error': 'Search query parameter "q" is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not request.user.is_staff:
            return Response(
                {'error': 'Permission denied'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        queryset = self.get_queryset().filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)





    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        """Toggle user active status (admin only)"""
        if not request.user.is_staff:
            return Response(
                {'error': 'Permission denied'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        user = self.get_object()
        
        # Prevent admin from deactivating themselves
        if user.id == request.user.id:
            return Response(
                {'error': 'Cannot deactivate your own account'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.is_active = not user.is_active
        user.save()
        
        serializer = self.get_serializer(user)
        return Response({
            'message': f'User {"activated" if user.is_active else "deactivated"} successfully',
            'user': serializer.data
        })


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for UserProfile model providing full CRUD operations.
    
    Available actions:
    - GET /api/profiles/ - List user profiles (admin only)
    - POST /api/profiles/ - Create a new profile
    - GET /api/profiles/{id}/ - Retrieve a specific profile
    - PUT /api/profiles/{id}/ - Update a profile (full update)
    - PATCH /api/profiles/{id}/ - Update a profile (partial update)
    - DELETE /api/profiles/{id}/ - Delete a profile
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__username', 'user__email', 'phone_number', 'address']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    def get_permissions(self):
        if self.action in ['list']:
            return [IsAdminUser()]
        return super().get_permissions()
    
    def get_queryset(self):
        """Filter queryset to show only current user's profile unless admin"""
        if self.request.user.is_staff:
            return UserProfile.objects.all()
        return UserProfile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Create a new profile"""
        serializer.save()

    def perform_update(self, serializer):
        """Update a profile"""
        serializer.save()

    def perform_destroy(self, instance):
        """Delete a profile"""
        instance.delete()
