"""
URL configuration for ecommerce_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app import views
    2. Add a URL to urlpatterns:  path('blog/', other_app.views.Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from . import views
from accounts.views import UserRegistrationView, UserLoginView
from .admin import admin_site
from . import crud_views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin_site.urls),
    
    # CRUD Dashboard URLs
    path('crud/', crud_views.crud_dashboard, name='crud-dashboard'),
    path('crud/products/', crud_views.crud_products, name='crud-products'),
    path('crud/categories/', crud_views.crud_categories, name='crud-categories'),
    path('crud/users/', crud_views.crud_users, name='crud-users'),
    
    # AJAX bulk operations
    path('crud/products/bulk-update/', crud_views.bulk_update_products, name='bulk-update-products'),
    path('crud/products/bulk-delete/', crud_views.bulk_delete_products, name='bulk-delete-products'),
    
    # API root endpoint - shows all available endpoints
    path('api/', views.api_root, name='api-root'),
    
    # JWT Authentication endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # User Authentication endpoints
    path('api/auth/register/', UserRegistrationView.as_view(), name='user-register'),
    path('api/auth/login/', UserLoginView.as_view(), name='user-login'),
    
    # API endpoints
    path('api/', include('accounts.urls')),
    path('api/', include('categories.urls')),
    path('api/', include('products.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
