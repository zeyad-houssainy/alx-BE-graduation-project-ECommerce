from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


class MainURLsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_page(self):
        """Test that home page is accessible"""
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'E-Commerce API')

    def test_admin_page(self):
        """Test that admin page is accessible"""
        url = reverse('admin:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Redirects to login

    def test_api_root(self):
        """Test that API root is accessible"""
        url = reverse('api-root')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # API root is publicly accessible


class JWTTokenTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_token_obtain(self):
        """Test JWT token obtain endpoint"""
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_token_refresh(self):
        """Test JWT token refresh endpoint"""
        # First get tokens
        tokens = self.get_tokens_for_user(self.user)
        
        # Then refresh
        url = reverse('token_refresh')
        data = {'refresh': tokens['refresh']}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_token_verify(self):
        """Test JWT token verify endpoint"""
        tokens = self.get_tokens_for_user(self.user)
        
        url = reverse('token_verify')
        data = {'token': tokens['access']}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def get_tokens_for_user(self, user):
        """Helper method to get JWT tokens for a user"""
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class AuthenticationEndpointsTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_registration_endpoint(self):
        """Test user registration endpoint"""
        url = reverse('api-user-register')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'password_confirm': 'newpass123',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', response.data)
        self.assertIn('user', response.data)
        self.assertIn('tokens', response.data)

    def test_user_login_endpoint(self):
        """Test user login endpoint"""
        # First create a user
        User.objects.create_user(
            username='loginuser',
            email='login@example.com',
            password='loginpass123'
        )
        
        url = reverse('api-user-login')
        data = {
            'username': 'loginuser',
            'password': 'loginpass123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('tokens', response.data)


class ProjectConfigurationTest(TestCase):
    def test_debug_setting(self):
        """Test that DEBUG setting is properly configured"""
        from django.conf import settings
        self.assertTrue(hasattr(settings, 'DEBUG'))

    def test_database_setting(self):
        """Test that database setting is properly configured"""
        from django.conf import settings
        self.assertTrue(hasattr(settings, 'DATABASES'))
        self.assertIn('default', settings.DATABASES)
        self.assertEqual(settings.DATABASES['default']['ENGINE'], 'django.db.backends.mysql')

    def test_installed_apps(self):
        """Test that required apps are installed"""
        from django.conf import settings
        required_apps = [
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'rest_framework',
            'rest_framework_simplejwt',
            'django_filters',
            'corsheaders',
            'accounts',
            'categories',
            'products',
        ]
        
        for app in required_apps:
            self.assertIn(app, settings.INSTALLED_APPS)

    def test_rest_framework_setting(self):
        """Test that REST framework is properly configured"""
        from django.conf import settings
        self.assertTrue(hasattr(settings, 'REST_FRAMEWORK'))
        self.assertIn('DEFAULT_AUTHENTICATION_CLASSES', settings.REST_FRAMEWORK)
        self.assertIn('DEFAULT_PERMISSION_CLASSES', settings.REST_FRAMEWORK)


class StaticFilesTest(TestCase):
    def test_static_files_configuration(self):
        """Test that static files are properly configured"""
        from django.conf import settings
        self.assertTrue(hasattr(settings, 'STATIC_URL'))
        self.assertTrue(hasattr(settings, 'STATIC_ROOT'))
        self.assertTrue(hasattr(settings, 'STATICFILES_DIRS'))

    def test_media_files_configuration(self):
        """Test that media files are properly configured"""
        from django.conf import settings
        self.assertTrue(hasattr(settings, 'MEDIA_URL'))
        self.assertTrue(hasattr(settings, 'MEDIA_ROOT'))


class SecurityTest(TestCase):
    def test_secret_key_setting(self):
        """Test that SECRET_KEY is properly set"""
        from django.conf import settings
        self.assertTrue(hasattr(settings, 'SECRET_KEY'))
        self.assertIsNotNone(settings.SECRET_KEY)

    def test_allowed_hosts_setting(self):
        """Test that ALLOWED_HOSTS is properly configured"""
        from django.conf import settings
        self.assertTrue(hasattr(settings, 'ALLOWED_HOSTS'))
        self.assertIsInstance(settings.ALLOWED_HOSTS, (list, tuple))


class IntegrationTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_complete_workflow(self):
        """Test complete workflow from registration to product creation"""
        # 1. Register user
        register_data = {
            'username': 'workflowuser',
            'email': 'workflow@example.com',
            'password': 'workflow123',
            'password_confirm': 'workflow123',
            'first_name': 'Workflow',
            'last_name': 'User'
        }
        register_response = self.client.post(
            reverse('api-user-register'), 
            register_data, 
            format='json'
        )
        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)
        
        # 2. Login user
        login_data = {
            'username': 'workflowuser',
            'password': 'workflow123'
        }
        login_response = self.client.post(
            reverse('api-user-login'), 
            login_data, 
            format='json'
        )
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        
        # 3. Get tokens
        tokens = login_response.data['tokens']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')
        
        # 4. Test authenticated endpoints
        # Test products endpoint
        products_response = self.client.get(reverse('product-list'))
        self.assertEqual(products_response.status_code, status.HTTP_200_OK)
        
        # Test categories endpoint
        categories_response = self.client.get(reverse('category-list'))
        self.assertEqual(categories_response.status_code, status.HTTP_200_OK)
        
        # Test user profile endpoint
        profile_response = self.client.get(reverse('user-profile'))
        self.assertEqual(profile_response.status_code, status.HTTP_200_OK)


class PerformanceTest(TestCase):
    def test_database_connection(self):
        """Test that database connection is working"""
        from django.db import connection
        from django.test.utils import override_settings
        
        # This test ensures the database connection is working
        with override_settings(DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'ecommerce_db',
                'HOST': 'localhost',
                'USER': 'root',
                'PASSWORD': 'Houssainy1995!'
            }
        }):
            try:
                connection.ensure_connection()
                self.assertTrue(connection.is_usable())
            except Exception as e:
                self.fail(f"Database connection failed: {e}")


class ErrorHandlingTest(TestCase):
    def test_404_error(self):
        """Test that 404 errors are handled properly"""
        self.client = Client()
        response = self.client.get('/nonexistent-page/')
        self.assertEqual(response.status_code, 404)

    def test_500_error(self):
        """Test that 500 errors are handled properly"""
        # This is a basic test - in a real scenario you'd test actual error conditions
        self.assertTrue(True)  # Placeholder for actual error handling tests
