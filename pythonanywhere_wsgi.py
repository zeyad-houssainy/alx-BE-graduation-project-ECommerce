"""
WSGI configuration for PythonAnywhere deployment.
This file should be placed in your PythonAnywhere web app configuration.
"""

import os
import sys

# Add your project directory to the Python path
# REPLACE 'zeyadhoussainy' with your actual PythonAnywhere username
path = '/home/zeyadhoussainy/alx-BE-graduation-project-ECommerce'
if path not in sys.path:
    sys.path.append(path)

# Set the Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'ecommerce_api.settings'

# Import Django WSGI application
try:
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
except Exception as e:
    # Log the error for debugging
    import logging
    logging.basicConfig(level=logging.DEBUG)
    logging.error(f"WSGI Error: {e}")
    raise
