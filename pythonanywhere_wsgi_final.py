"""
WSGI configuration for PythonAnywhere deployment.
Copy this content to your PythonAnywhere WSGI file.
"""

import os
import sys

# Add your project directory to the Python path
path = '/home/zeyadhoussainy/alx-BE-graduation-project-ECommerce'
if path not in sys.path:
    sys.path.insert(0, path)

# Set the Django settings module - THIS IS THE CRITICAL FIX
os.environ['DJANGO_SETTINGS_MODULE'] = 'ecommerce_api.settings'

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
