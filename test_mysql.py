#!/usr/bin/env python3
"""
MySQL Connection Test Script
This script helps you test your MySQL connection and diagnose issues.
"""

import os
from decouple import config
import pymysql

def test_mysql_connection():
    """Test MySQL connection using environment variables."""
    
    print("=== MySQL Connection Test ===\n")
    
    # Try to get database configuration from environment
    try:
        db_name = config('DB_NAME', default='ecommerce_db')
        db_host = config('DB_HOST', default='localhost')
        db_user = config('DB_USER', default='root')
        db_password = config('DB_PASSWORD', default='')
        db_port = config('DB_PORT', default=3306, cast=int)
        
        print(f"Database Configuration:")
        print(f"  Host: {db_host}")
        print(f"  Port: {db_port}")
        print(f"  Database: {db_name}")
        print(f"  User: {db_user}")
        print(f"  Password: {'*' * len(db_password) if db_password else 'None'}")
        print()
        
    except Exception as e:
        print(f"❌ Error reading environment variables: {e}")
        print("Make sure you have a .env file with database credentials")
        return
    
    # Test connection
    try:
        print("Testing connection...")
        connection = pymysql.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
            database=db_name,
            charset='utf8mb4'
        )
        
        if connection.open:
            print("✅ MySQL connection successful!")
            
            # Test basic operations
            with connection.cursor() as cursor:
                cursor.execute("SELECT VERSION()")
                version = cursor.fetchone()
                print(f"✅ MySQL version: {version[0]}")
                
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                if tables:
                    print(f"✅ Found {len(tables)} tables in database")
                else:
                    print("ℹ️  No tables found (this is normal for a new database)")
            
            connection.close()
            print("\n🎉 All tests passed! Your MySQL setup is working correctly.")
            
        else:
            print("❌ Connection failed")
            
    except pymysql.Error as e:
        print(f"❌ MySQL Error: {e}")
        print("\nTroubleshooting:")
        
        if "Access denied" in str(e):
            print("1. Check username and password")
            print("2. Verify user has access to the database")
            print("3. Try connecting as root first")
            
        elif "Can't connect" in str(e):
            print("1. Make sure MySQL service is running")
            print("2. Check if MySQL is listening on the correct port")
            print("3. Verify firewall settings")
            
        elif "Unknown database" in str(e):
            print("1. Create the database first")
            print("2. Check database name spelling")
            print("3. Run: CREATE DATABASE ecommerce_db;")
            
        elif "authentication plugin" in str(e):
            print("1. This is a common PyMySQL issue")
            print("2. Try using mysql-connector-python instead")
            print("3. Or change MySQL user authentication method")
            
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print("Check your Python environment and dependencies")

def test_root_connection():
    """Test connection as root user."""
    
    print("\n=== Testing Root Connection ===\n")
    
    root_password = input("Enter MySQL root password (or press Enter if none): ")
    
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password=root_password if root_password else None,
            charset='utf8mb4'
        )
        
        if connection.open:
            print("✅ Root connection successful!")
            
            with connection.cursor() as cursor:
                cursor.execute("SHOW DATABASES")
                databases = cursor.fetchall()
                print(f"Available databases: {[db[0] for db in databases]}")
            
            connection.close()
            return True
            
        else:
            print("❌ Root connection failed")
            return False
            
    except pymysql.Error as e:
        print(f"❌ Root connection error: {e}")
        return False

if __name__ == "__main__":
    print("This script will test your MySQL connection.\n")
    
    # First test with environment variables
    test_mysql_connection()
    
    # Optionally test root connection
    print("\n" + "="*50)
    test_root = input("\nWould you like to test root connection? (y/n): ").lower().strip()
    
    if test_root == 'y':
        test_root_connection()
    
    print("\n" + "="*50)
    print("\nNext steps:")
    print("1. If connection failed, check the troubleshooting tips above")
    print("2. Make sure MySQL service is running")
    print("3. Verify your .env file has correct credentials")
    print("4. Run: python setup_mysql.py (for automated setup)")
    print("5. Or follow the manual setup in MYSQL_SETUP_GUIDE.md")
