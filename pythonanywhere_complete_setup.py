#!/usr/bin/env python3
"""
Complete setup script for PythonAnywhere deployment
Run this script in the PythonAnywhere bash console
"""

import os
import sys
import socket
import subprocess

def run_command(command, description):
    """Run a command and return the result"""
    print(f"\n🔄 {description}")
    print(f"Running: {command}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - SUCCESS")
            if result.stdout:
                print(f"Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {description} - FAILED")
            print(f"Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ {description} - EXCEPTION: {e}")
        return False

def check_environment():
    """Check if we're running on PythonAnywhere"""
    hostname = socket.gethostname()
    is_pythonanywhere = 'pythonanywhere.com' in hostname or 'liveconsole' in hostname
    
    print("🔍 Environment Check:")
    print(f"   Hostname: {hostname}")
    print(f"   PythonAnywhere: {is_pythonanywhere}")
    
    return is_pythonanywhere

def create_static_directory():
    """Create static directory structure"""
    print("\n📁 Creating static directory structure...")
    
    project_path = '/home/zeyadhoussainy/alx-BE-graduation-project-ECommerce'
    static_dir = os.path.join(project_path, 'static')
    
    if not os.path.exists(static_dir):
        os.makedirs(static_dir, exist_ok=True)
        print(f"✅ Created: {static_dir}")
        
        # Create subdirectories
        for subdir in ['css', 'js', 'images']:
            subdir_path = os.path.join(static_dir, subdir)
            os.makedirs(subdir_path, exist_ok=True)
            print(f"✅ Created: {subdir_path}")
    else:
        print(f"✅ Static directory already exists: {static_dir}")

def setup_database():
    """Setup database and run migrations"""
    print("\n🗄️ Setting up database...")
    
    project_path = '/home/zeyadhoussainy/alx-BE-graduation-project-ECommerce'
    os.chdir(project_path)
    
    # Run migrations
    run_command("python manage.py makemigrations", "Creating new migrations")
    run_command("python manage.py migrate", "Running database migrations")
    
    # Create mock users
    run_command("python manage.py create_mock_users", "Creating mock users and admin")

def collect_static_files():
    """Collect static files"""
    print("\n📦 Collecting static files...")
    run_command("python manage.py collectstatic --noinput", "Collecting static files")

def check_admin_credentials():
    """Display admin credentials"""
    print("\n👤 Admin Credentials:")
    print("   Username: admin")
    print("   Password: admin")
    print("   Django Admin: https://zeyadhoussainy.pythonanywhere.com/admin/")

def main():
    """Main setup function"""
    print("🚀 PythonAnywhere Django Project Setup")
    print("=" * 50)
    
    # Check environment
    if not check_environment():
        print("⚠️  Warning: This script is designed for PythonAnywhere")
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    # Setup steps
    create_static_directory()
    setup_database()
    collect_static_files()
    check_admin_credentials()
    
    print("\n🎉 Setup Complete!")
    print("=" * 50)
    print("Next steps:")
    print("1. Test your website: https://zeyadhoussainy.pythonanywhere.com")
    print("2. Access admin panel: https://zeyadhoussainy.pythonanywhere.com/admin/")
    print("3. Check API endpoints: https://zeyadhoussainy.pythonanywhere.com/api/")

if __name__ == '__main__':
    main()
