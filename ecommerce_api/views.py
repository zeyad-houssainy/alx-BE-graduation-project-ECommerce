from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import status

def home(request):
    """Home page view"""
    return render(request, 'home.html')

@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    """API root endpoint showing all available endpoints"""
    
    # Base URL for the API
    base_url = request.build_absolute_uri('/api/')
    
    # Available endpoints
    endpoints = {
        'authentication': {
            'description': 'User authentication and management',
            'endpoints': {
                'register': {
                    'url': reverse('user-register', request=request),
                    'method': 'POST',
                    'description': 'Create a new user account',
                    'auth_required': False,
                    'example_data': {
                        'username': 'newuser',
                        'email': 'user@example.com',
                        'password': 'securepassword123',
                        'password_confirm': 'securepassword123',
                        'first_name': 'John',
                        'last_name': 'Doe'
                    }
                },
                'login': {
                    'url': reverse('user-login', request=request),
                    'method': 'POST',
                    'description': 'Authenticate user and get JWT tokens',
                    'auth_required': False,
                    'example_data': {
                        'username': 'admin',
                        'password': 'admin123'
                    }
                },
                'token_refresh': {
                    'url': reverse('token_refresh', request=request),
                    'method': 'POST',
                    'description': 'Refresh JWT access token',
                    'auth_required': False,
                    'example_data': {
                        'refresh': 'your_refresh_token_here'
                    }
                },
                'token_verify': {
                    'url': reverse('token_verify', request=request),
                    'method': 'POST',
                    'description': 'Verify JWT token validity',
                    'auth_required': False,
                    'example_data': {
                        'token': 'your_access_token_here'
                    }
                }
            }
        },
        'products': {
            'description': 'Product management and information',
            'endpoints': {
                'list_products': {
                    'url': base_url + 'products/',
                    'method': 'GET',
                    'description': 'Get all products (public)',
                    'auth_required': False,
                    'filters': '?search=keyword&category=1&price__gte=100&price__lte=500'
                },
                'product_detail': {
                    'url': base_url + 'products/{slug}/',
                    'method': 'GET',
                    'description': 'Get specific product details (public)',
                    'auth_required': False
                },
                'create_product': {
                    'url': base_url + 'products/',
                    'method': 'POST',
                    'description': 'Create a new product',
                    'auth_required': True,
                    'example_data': {
                        'name': 'New Product',
                        'description': 'Product description',
                        'price': '99.99',
                        'category': 1,
                        'stock_quantity': 50,
                        'image': 'image_file'
                    }
                },
                'update_product': {
                    'url': base_url + 'products/{slug}/',
                    'method': 'PUT',
                    'description': 'Update product information',
                    'auth_required': True
                },
                'delete_product': {
                    'url': base_url + 'products/{slug}/',
                    'method': 'DELETE',
                    'description': 'Delete a product',
                    'auth_required': True
                }
            }
        },
        'categories': {
            'description': 'Product category management',
            'endpoints': {
                'list_categories': {
                    'url': base_url + 'categories/',
                    'method': 'GET',
                    'description': 'Get all categories (public)',
                    'auth_required': False
                },
                'category_detail': {
                    'url': base_url + 'categories/{slug}/',
                    'method': 'GET',
                    'description': 'Get specific category details (public)',
                    'auth_required': False
                },
                'create_category': {
                    'url': base_url + 'categories/',
                    'method': 'POST',
                    'description': 'Create a new category',
                    'auth_required': True,
                    'example_data': {
                        'name': 'New Category',
                        'description': 'Category description',
                        'image': 'image_file'
                    }
                },
                'update_category': {
                    'url': base_url + 'categories/{slug}/',
                    'method': 'PUT',
                    'description': 'Update category information',
                    'auth_required': True
                },
                'delete_category': {
                    'url': base_url + 'categories/{slug}/',
                    'method': 'DELETE',
                    'description': 'Delete a category',
                    'auth_required': True
                }
            }
        },
        'users': {
            'description': 'User management and profiles',
            'endpoints': {
                'list_users': {
                    'url': base_url + 'users/',
                    'method': 'GET',
                    'description': 'Get all users',
                    'auth_required': True
                },
                'user_detail': {
                    'url': base_url + 'users/{id}/',
                    'method': 'GET',
                    'description': 'Get specific user details',
                    'auth_required': True
                },
                'user_profile': {
                    'url': base_url + 'users/profile/',
                    'method': 'GET',
                    'description': 'Get current user profile',
                    'auth_required': True
                },
                'update_profile': {
                    'url': base_url + 'users/update_profile/',
                    'method': 'PUT',
                    'description': 'Update current user profile',
                    'auth_required': True
                },
                'profiles': {
                    'url': base_url + 'profiles/',
                    'method': 'GET',
                    'description': 'Get all user profiles',
                    'auth_required': True
                }
            }
        }
    }
    
    # API information
    api_info = {
        'name': 'E-Commerce API',
        'version': '1.0.0',
        'description': 'A comprehensive e-commerce API built with Django REST Framework',
        'base_url': base_url,
        'authentication': 'JWT (JSON Web Tokens)',
        'documentation': 'All endpoints support the browsable API interface',
        'endpoints': endpoints,
        'usage_instructions': {
            'public_endpoints': 'These endpoints can be accessed without authentication',
            'protected_endpoints': 'These endpoints require a valid JWT token in the Authorization header',
            'authentication_header': 'Authorization: Bearer <your_access_token>',
            'example_curl': 'curl -H "Authorization: Bearer <token>" http://127.0.0.1:8000/api/products/'
        }
    }
    
    return Response(api_info, status=status.HTTP_200_OK)
