"""
WSGI configuration for PythonAnywhere deployment.
This file should be placed in your PythonAnywhere web app configuration.
"""

import os
import sys

# Add your project directory to the Python path
path = '/home/yourusername/alx-BE-graduation-project-ECommerce'
if path not in sys.path:
    sys.path.append(path)

# Set the Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'ecommerce_api.settings'

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
