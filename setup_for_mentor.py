#!/usr/bin/env python3
"""
Setup Script for Mentors & Reviewers
This script helps mentors quickly set up and test the e-commerce project.
"""

import os
import sys
import subprocess
import time

def run_command(command, description):
    """Run a command and handle errors gracefully"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def check_prerequisites():
    """Check if required tools are installed"""
    print("🔍 Checking prerequisites...")
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 11):
        print("❌ Python 3.11+ is required")
        print(f"Current version: {python_version.major}.{python_version.minor}.{python_version.micro}")
        return False
    
    print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro} ✓")
    
    # Check if pip is available
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], check=True, capture_output=True)
        print("✅ pip is available ✓")
    except subprocess.CalledProcessError:
        print("❌ pip is not available")
        return False
    
    # Check if virtual environment exists
    if os.path.exists(".venv"):
        print("✅ Virtual environment exists ✓")
    else:
        print("⚠️  Virtual environment not found (will be created)")
    
    return True

def setup_virtual_environment():
    """Create and activate virtual environment"""
    if not os.path.exists(".venv"):
        print("\n🐍 Creating virtual environment...")
        if not run_command(f"{sys.executable} -m venv .venv", "Creating virtual environment"):
            return False
    
    # Activate virtual environment
    if os.name == 'nt':  # Windows
        activate_script = ".venv\\Scripts\\activate"
        python_path = ".venv\\Scripts\\python.exe"
        pip_path = ".venv\\Scripts\\pip.exe"
    else:  # Unix/Linux/Mac
        activate_script = ".venv/bin/activate"
        python_path = ".venv/bin/python"
        pip_path = ".venv/bin/pip"
    
    print(f"✅ Virtual environment ready at: {python_path}")
    return python_path, pip_path

def install_dependencies(pip_path):
    """Install project dependencies"""
    print("\n📦 Installing dependencies...")
    if not run_command(f"{pip_path} install -r requirements.txt", "Installing dependencies"):
        return False
    return True

def setup_database(python_path):
    """Setup database with migrations"""
    print("\n🗄️  Setting up database...")
    
    # Check if .env file exists
    if not os.path.exists(".env"):
        print("⚠️  .env file not found. Please create it from env_example.txt")
        print("Make sure to set your MySQL database credentials")
        return False
    
    # Run migrations
    if not run_command(f"{python_path} manage.py makemigrations", "Creating migrations"):
        return False
    
    if not run_command(f"{python_path} manage.py migrate", "Applying migrations"):
        return False
    
    return True

def create_superuser(python_path):
    """Create a superuser for admin access"""
    print("\n👤 Creating superuser...")
    print("Please enter the following details:")
    
    # Create a default superuser
    superuser_data = {
        "username": "mentor",
        "email": "mentor@example.com",
        "password": "mentor123"
    }
    
    # Use Django shell to create superuser
    create_user_script = f"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_api.settings')
django.setup()

from django.contrib.auth.models import User
if not User.objects.filter(username='{superuser_data["username"]}').exists():
    user = User.objects.create_superuser(
        username='{superuser_data["username"]}',
        email='{superuser_data["email"]}',
        password='{superuser_data["password"]}'
    )
    print(f'Superuser created: {{user.username}}')
else:
    print('Superuser already exists')
"""
    
    with open("temp_create_user.py", "w") as f:
        f.write(create_user_script)
    
    if run_command(f"{python_path} temp_create_user.py", "Creating superuser"):
        os.remove("temp_create_user.py")
        print(f"✅ Superuser created:")
        print(f"   Username: {superuser_data['username']}")
        print(f"   Password: {superuser_data['password']}")
        return True
    
    return False

def generate_sample_data(python_path):
    """Generate sample data for testing"""
    print("\n📊 Generating sample data...")
    
    # Try to generate large dataset first
    if run_command(f"{python_path} manage.py generate_large_dataset --clear", "Generating large dataset"):
        print("✅ Generated 500+ products and 200+ users")
        return True
    
    # Fallback to basic sample data
    if run_command(f"{python_path} manage.py create_sample_data", "Generating basic sample data"):
        print("✅ Generated basic sample data")
        return True
    
    print("⚠️  Could not generate sample data. You can do this manually later.")
    return True

def run_tests(python_path):
    """Run project tests"""
    print("\n🧪 Running tests...")
    if run_command(f"{python_path} manage.py test", "Running tests"):
        print("✅ All tests passed!")
        return True
    else:
        print("⚠️  Some tests failed. Check the output above.")
        return True

def start_server(python_path):
    """Start the development server"""
    print("\n🚀 Starting development server...")
    print("The server will start in the background.")
    print("You can access:")
    print("  - API: http://127.0.0.1:8000/api/")
    print("  - Admin: http://127.0.0.1:8000/admin/")
    print("  - Home: http://127.0.0.1:8000/")
    print("\nPress Ctrl+C to stop the server when done.")
    
    try:
        subprocess.run([python_path, "manage.py", "runserver"], check=True)
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Server failed to start: {e}")

def main():
    """Main setup function"""
    print("🎯 E-Commerce Project Setup for Mentors")
    print("=" * 50)
    
    # Check prerequisites
    if not check_prerequisites():
        print("\n❌ Prerequisites check failed. Please install required tools.")
        return
    
    # Setup virtual environment
    result = setup_virtual_environment()
    if not result:
        print("\n❌ Virtual environment setup failed.")
        return
    
    python_path, pip_path = result
    
    # Install dependencies
    if not install_dependencies(pip_path):
        print("\n❌ Dependency installation failed.")
        return
    
    # Setup database
    if not setup_database(python_path):
        print("\n❌ Database setup failed.")
        return
    
    # Create superuser
    if not create_superuser(python_path):
        print("\n❌ Superuser creation failed.")
        return
    
    # Generate sample data
    if not generate_sample_data(python_path):
        print("\n❌ Sample data generation failed.")
        return
    
    # Run tests
    run_tests(python_path)
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Visit http://127.0.0.1:8000/admin/")
    print("2. Login with username: 'mentor' and password: 'mentor123'")
    print("3. Explore the enhanced admin interface")
    print("4. Test API endpoints at http://127.0.0.1:8000/api/")
    
    # Ask if user wants to start server
    response = input("\n🚀 Would you like to start the development server now? (y/n): ")
    if response.lower() in ['y', 'yes']:
        start_server(python_path)
    else:
        print("\n💡 To start the server later, run:")
        print(f"   {python_path} manage.py runserver")

if __name__ == "__main__":
    main()
