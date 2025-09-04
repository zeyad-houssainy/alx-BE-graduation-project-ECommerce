#!/usr/bin/env python3
"""
MySQL Setup Script for Django E-commerce API
This script helps you set up the MySQL database for local development.
"""

import mysql.connector
from mysql.connector import Error
import getpass
import subprocess
import sys
import os

def check_mysql_service():
    """Check if MySQL service is running."""
    print("Checking MySQL service status...")
    
    try:
        # Try to connect to MySQL without specifying database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            port=3306
        )
        if connection.is_connected():
            print("✅ MySQL service is running")
            connection.close()
            return True
    except:
        pass
    
    try:
        # Try with common default passwords
        test_passwords = ["", "root", "password", "admin", "123456"]
        for pwd in test_passwords:
            try:
                connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password=pwd,
                    port=3306
                )
                if connection.is_connected():
                    print(f"✅ MySQL service is running (root password: {pwd if pwd else 'none'})")
                    connection.close()
                    return True, pwd
            except:
                continue
    except:
        pass
    
    print("❌ MySQL service is not running or not accessible")
    print("\nTroubleshooting:")
    print("1. Make sure MySQL is installed")
    print("2. Start MySQL service:")
    print("   - Windows: Check Services app for MySQL")
    print("   - macOS: brew services start mysql")
    print("   - Linux: sudo systemctl start mysql")
    return False

def create_database_and_user():
    """Create database and user for the Django application."""
    
    print("=== MySQL Setup for Django E-commerce API ===\n")
    
    # First check if MySQL service is running
    service_status = check_mysql_service()
    if not service_status:
        return False
    
    # Get MySQL root password
    root_password = getpass.getpass("Enter MySQL root password (or press Enter if no password): ")
    
    # Database configuration
    db_name = "ecommerce_db"
    db_user = "ecommerce_user"
    db_password = getpass.getpass(f"Enter password for new user '{db_user}': ")
    
    try:
        # Connect to MySQL as root
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=root_password if root_password else None,
            port=3306
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Create database
            print(f"\nCreating database '{db_name}'...")
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"✅ Database '{db_name}' created successfully!")
            
            # Create user
            print(f"\nCreating user '{db_user}'...")
            try:
                cursor.execute(f"CREATE USER IF NOT EXISTS '{db_user}'@'localhost' IDENTIFIED BY '{db_password}'")
                print(f"✅ User '{db_user}' created successfully!")
            except Error as e:
                if "already exists" in str(e).lower():
                    print(f"ℹ️  User '{db_user}' already exists, updating password...")
                    cursor.execute(f"ALTER USER '{db_user}'@'localhost' IDENTIFIED BY '{db_password}'")
                    print(f"✅ User '{db_user}' password updated successfully!")
                else:
                    raise e
            
            # Grant privileges
            print(f"\nGranting privileges to '{db_user}'...")
            cursor.execute(f"GRANT ALL PRIVILEGES ON {db_name}.* TO '{db_user}'@'localhost'")
            cursor.execute("FLUSH PRIVILEGES")
            print(f"✅ Privileges granted successfully!")
            
            # Test connection with new user
            print(f"\nTesting connection with new user...")
            test_connection = mysql.connector.connect(
                host="localhost",
                user=db_user,
                password=db_password,
                database=db_name,
                port=3306
            )
            
            if test_connection.is_connected():
                print("✅ Connection test successful!")
                test_connection.close()
            else:
                print("❌ Connection test failed!")
            
            print("\n=== Setup Complete! ===")
            print(f"Database: {db_name}")
            print(f"User: {db_user}")
            print(f"Host: localhost")
            print(f"Port: 3306")
            
            # Create .env file automatically
            create_env_file(db_name, db_user, db_password)
            
            print("\n=== Next Steps ===")
            print("1. .env file has been created automatically")
            print("2. Run: python manage.py migrate")
            print("3. Run: python manage.py runserver")
            
            return True
            
    except Error as e:
        print(f"❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure MySQL is running")
        print("2. Check if root password is correct")
        print("3. Ensure MySQL user has CREATE privileges")
        print("4. Try running as administrator/with sudo")
        
        # Try alternative connection methods
        print("\nTrying alternative connection methods...")
        try_alternative_connections()
        
        return False
        
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

def try_alternative_connections():
    """Try alternative connection methods."""
    print("\n=== Alternative Connection Methods ===")
    
    # Method 1: Try without password
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            port=3306
        )
        if connection.is_connected():
            print("✅ Success: Connected as root without password")
            connection.close()
            return
    except:
        pass
    
    # Method 2: Try with socket file (Unix-like systems)
    try:
        connection = mysql.connector.connect(
            unix_socket="/tmp/mysql.sock",
            user="root",
            port=3306
        )
        if connection.is_connected():
            print("✅ Success: Connected via socket file")
            connection.close()
            return
    except:
        pass
    
    # Method 3: Try different ports
    for port in [3306, 3307, 3308]:
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                port=port
            )
            if connection.is_connected():
                print(f"✅ Success: Connected on port {port}")
                connection.close()
                return
        except:
            continue
    
    print("❌ All connection methods failed")
    print("Please check your MySQL installation and configuration")

def create_env_file(db_name, db_user, db_password):
    """Create .env file with database credentials."""
    env_content = f"""# Django Settings
SECRET_KEY=django-insecure-local-development-key-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
RAILWAY_ENVIRONMENT=False

# MySQL Database Configuration
DB_NAME={db_name}
DB_HOST=localhost
DB_USER={db_user}
DB_PASSWORD={db_password}
DB_PORT=3306

# Alternative MySQL Variables
MYSQLDATABASE={db_name}
MYSQLHOST=localhost
MYSQLUSERNAME={db_user}
MYSQLPASSWORD={db_password}
MYSQLPORT=3306

# Security Settings (False for local development)
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False

# JWT Settings
JWT_SECRET_KEY=local-jwt-secret-key-change-in-production
JWT_ACCESS_TOKEN_LIFETIME=1
JWT_REFRESH_TOKEN_LIFETIME=7

# CORS Settings for Local Development
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://localhost:8080,http://127.0.0.1:8080

# Static and Media Files
STATIC_ROOT=staticfiles
MEDIA_ROOT=media

# Logging
LOG_LEVEL=DEBUG
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ .env file created successfully with your database credentials!")
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        print("Please create .env file manually using env.example as template")

def install_dependencies():
    """Install required Python dependencies."""
    print("\n=== Installing Dependencies ===")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def run_migrations():
    """Run Django migrations."""
    print("\n=== Running Database Migrations ===")
    try:
        subprocess.check_call([sys.executable, "manage.py", "migrate"])
        print("✅ Migrations completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running migrations: {e}")
        return False

def main():
    """Main setup function."""
    print("🚀 Django E-commerce API - Complete Setup")
    print("=" * 50)
    
    # Step 1: Install dependencies
    if not install_dependencies():
        print("❌ Setup failed at dependency installation")
        return
    
    # Step 2: Setup MySQL
    if not create_database_and_user():
        print("❌ Setup failed at MySQL setup")
        return
    
    # Step 3: Run migrations
    if not run_migrations():
        print("❌ Setup failed at migrations")
        return
    
    print("\n🎉 Setup completed successfully!")
    print("\n=== Your project is ready! ===")
    print("1. Database: MySQL configured and connected")
    print("2. Environment: .env file created with credentials")
    print("3. Django: Migrations completed")
    print("\nTo start the development server:")
    print("python manage.py runserver")
    print("\nTo create a superuser:")
    print("python manage.py createsuperuser")

if __name__ == "__main__":
    main()
