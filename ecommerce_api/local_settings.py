# Local development settings
# This file should not be committed to version control

# Import BASE_DIR from main settings
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

# Override settings for local development

# Database Configuration for MySQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ecommerce_db',
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': 'Houssainy1995!',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# Override secret key for development
SECRET_KEY = 'django-insecure-s8md8r=z3^2w8aud0buw4bvpe1uy%l#n=p30it8ozh7981cp47'

# Debug settings
DEBUG = True

# Allowed hosts
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Email settings for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Static and media files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# MySQL specific settings
DATABASE_OPTIONS = {
    'charset': 'utf8mb4',
    'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
}
