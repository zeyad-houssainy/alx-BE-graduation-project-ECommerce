#!/usr/bin/env python3
"""
PythonAnywhere Setup Script
Run this script on PythonAnywhere to set up your Django project
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ Error in {description}: {e}")
        print(f"Error output: {e.stderr}")
        return None

def create_env_file():
    """Create the .env file with correct PythonAnywhere settings"""
    env_content = """# PythonAnywhere Environment Variables
# Production configuration for zeyadhoussainy.pythonanywhere.com

# Django Settings
SECRET_KEY=django-insecure-production-key-change-this-immediately
DEBUG=False
ALLOWED_HOSTS=*
PYTHONANYWHERE_ENVIRONMENT=True

# Database Configuration (PythonAnywhere MySQL)
DB_NAME=zeyadhoussainy$ecommerce_db
DB_HOST=zeyadhoussainy.mysql.pythonanywhere-services.com
DB_USER=zeyadhoussainy
DB_PASSWORD=your-database-password-here
DB_PORT=3306

# JWT Authentication
JWT_SECRET_KEY=your-jwt-secret-key-change-this-immediately

# CORS Settings
CORS_ALLOWED_ORIGINS=https://zeyadhoussainy.pythonanywhere.com

# Security Settings (Production)
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_SSL_REDIRECT=True

# Static and Media Files
STATIC_ROOT=/home/zeyadhoussainy/alx-BE-graduation-project-ECommerce/staticfiles
MEDIA_ROOT=/home/zeyadhoussainy/alx-BE-graduation-project-ECommerce/media

# Logging
LOG_LEVEL=INFO
"""
    
    env_file = '.env'
    if not os.path.exists(env_file):
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ .env file created")
        print("⚠️  IMPORTANT: Update the database password and secret keys!")
    else:
        print("⚠️  .env file already exists - check if it has correct values")

def main():
    print("🚀 PythonAnywhere Django Project Setup")
    print("=" * 50)
    
    # Get project directory
    project_dir = os.getcwd()
    print(f"📁 Project directory: {project_dir}")
    
    # Check if we're in the right directory
    if not os.path.exists('manage.py'):
        print("❌ Error: manage.py not found. Please run this script from your Django project directory.")
        return
    
    # Create .env file
    print("\n🔧 Creating environment file...")
    create_env_file()
    
    # Install requirements
    print("\n📦 Installing Python dependencies...")
    run_command("pip install --user -r requirements.txt", "Installing requirements")
    
    # Run migrations
    print("\n🗄️  Running database migrations...")
    run_command("python manage.py migrate", "Running migrations")
    
    # Collect static files
    print("\n📁 Collecting static files...")
    run_command("python manage.py collectstatic --noinput", "Collecting static files")
    
    # Create superuser if needed
    print("\n👤 Superuser creation...")
    print("   Run 'python manage.py createsuperuser' manually if needed")
    
    print("\n🎉 Setup completed!")
    print("\n📋 Next steps:")
    print("1. Update your .env file with correct database password and secret keys")
    print("2. In your PythonAnywhere web app configuration:")
    print("   - Set WSGI file path to: pythonanywhere_wsgi_corrected.py")
    print("   - Or update the existing WSGI file with correct Django settings module")
    print("3. Reload your web app")
    print("\n🔧 WSGI Fix Required:")
    print("   Change 'alx-BE-graduation-project-ECommerce.settings' to 'ecommerce_api.settings'")

if __name__ == "__main__":
    main()
