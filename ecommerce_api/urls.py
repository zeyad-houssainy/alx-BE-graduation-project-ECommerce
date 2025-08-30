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

from .admin import admin_site
from . import crud_views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin_site.urls),
    
    # Healthcheck endpoint for Railway
    path('health/', views.healthcheck, name='healthcheck'),
    
    # Authentication URLs
    path('login/', views.user_login, name='user-login'),
    path('logout/', views.user_logout, name='user-logout'),
    path('register/', views.user_register, name='user-register'),
    path('profile/', views.profile, name='user-profile'),
    
    # CRUD Dashboard URLs
    path('crud/', crud_views.crud_dashboard, name='crud-dashboard'),
    path('crud/products/', crud_views.crud_products, name='crud-products'),
    path('crud/categories/', crud_views.crud_categories, name='crud-categories'),
    path('crud/users/', crud_views.crud_users, name='crud-users'),
    

    
    # API root endpoint - shows all available endpoints
    path('api/', views.api_root, name='api-root'),
    
    # JWT Authentication endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # User Authentication endpoints (handled by accounts.urls)
    
    # API endpoints
    path('api/', include('accounts.urls')),
    path('api/', include('categories.urls')),
    path('api/', include('products.urls')),
    
    # Documentation
    path('docs/', views.documentation, name='documentation'),
    
    # Mock data creation
    path('create-mock-data/', views.create_mock_data, name='create-mock-data'),
    path('create-mock-users/', views.create_mock_users, name='create-mock-users'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    # In production, PythonAnywhere handles static files automatically
# Media files should be served through a CDN or separate service
pass
