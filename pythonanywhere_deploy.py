#!/usr/bin/env python3
"""
PythonAnywhere Deployment Script
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

def main():
    print("🚀 PythonAnywhere Django Project Setup")
    print("=" * 50)
    
    # Check if we're on PythonAnywhere
    if 'PYTHONANYWHERE_SITE' not in os.environ:
        print("⚠️  This script is designed to run on PythonAnywhere")
        print("   Please run it in your PythonAnywhere bash console")
        return
    
    # Get project directory
    project_dir = os.getcwd()
    print(f"📁 Project directory: {project_dir}")
    
    # Install requirements
    print("\n📦 Installing Python dependencies...")
    run_command("pip install --user -r requirements.txt", "Installing PythonAnywhere-optimized requirements")
    
    # Create .env file if it doesn't exist
    env_file = os.path.join(project_dir, '.env')
    if not os.path.exists(env_file):
        print("\n🔧 Creating .env file...")
        env_content = """# PythonAnywhere Environment Variables
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourusername.pythonanywhere.com
DB_NAME=yourusername$ecommerce_db
DB_HOST=yourusername.mysql.pythonanywhere-services.com
DB_USER=yourusername
DB_PASSWORD=your-database-password
DB_PORT=3306
JWT_SECRET_KEY=your-jwt-secret-here
CORS_ALLOWED_ORIGINS=https://yourusername.pythonanywhere.com
"""
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ .env file created")
        print("⚠️  Please update the .env file with your actual values")
    
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
    print("1. Update your .env file with correct values")
    print("2. Configure your PythonAnywhere web app")
    print("3. Set the WSGI file path to: pythonanywhere_wsgi.py")
    print("4. Reload your web app")

if __name__ == "__main__":
    main()
