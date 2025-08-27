#!/usr/bin/env python3
"""
Database Creation Script for Django E-commerce API
This script creates the MySQL database and handles database-related issues.
"""

import mysql.connector
from mysql.connector import Error
import getpass
import sys

def create_database():
    """Create the ecommerce_db database."""
    print("=== Creating MySQL Database ===")
    
    # Get MySQL root password
    root_password = getpass.getpass("Enter MySQL root password (or press Enter if none): ")
    
    try:
        # Connect to MySQL as root (without specifying database)
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=root_password if root_password else None,
            port=3306
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Create database
            db_name = "ecommerce_db"
            print(f"\nCreating database '{db_name}'...")
            
            try:
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                print(f"✅ Database '{db_name}' created successfully!")
            except Error as e:
                if "already exists" in str(e).lower():
                    print(f"ℹ️  Database '{db_name}' already exists")
                else:
                    print(f"❌ Error creating database: {e}")
                    return False
            
            # Show all databases
            cursor.execute("SHOW DATABASES")
            databases = cursor.fetchall()
            print(f"\nAvailable databases:")
            for db in databases:
                if db[0] == db_name:
                    print(f"  ✅ {db[0]} (your database)")
                else:
                    print(f"  ℹ️  {db[0]}")
            
            # Test connection to the new database
            print(f"\nTesting connection to '{db_name}'...")
            test_connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password=root_password if root_password else None,
                database=db_name,
                port=3306
            )
            
            if test_connection.is_connected():
                print(f"✅ Successfully connected to '{db_name}'")
                test_connection.close()
            else:
                print(f"❌ Failed to connect to '{db_name}'")
                return False
            
            print(f"\n🎉 Database '{db_name}' is ready!")
            return True
            
        else:
            print("❌ Failed to connect to MySQL")
            return False
            
    except Error as e:
        print(f"❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure MySQL is running")
        print("2. Check if root password is correct")
        print("3. Ensure MySQL user has CREATE privileges")
        return False
        
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

def create_dedicated_user():
    """Create a dedicated user for the application."""
    print("\n=== Creating Dedicated User ===")
    
    # Get MySQL root password
    root_password = getpass.getpass("Enter MySQL root password (or press Enter if none): ")
    
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
            
            # Create user
            db_user = "ecommerce_user"
            db_password = getpass.getpass(f"Enter password for new user '{db_user}': ")
            
            try:
                cursor.execute(f"CREATE USER IF NOT EXISTS '{db_user}'@'localhost' IDENTIFIED BY '{db_password}'")
                print(f"✅ User '{db_user}' created successfully!")
            except Error as e:
                if "already exists" in str(e).lower():
                    print(f"ℹ️  User '{db_user}' already exists, updating password...")
                    cursor.execute(f"ALTER USER '{db_user}'@'localhost' IDENTIFIED BY '{db_password}'")
                    print(f"✅ User '{db_user}' password updated successfully!")
                else:
                    print(f"❌ Error creating user: {e}")
                    return False
            
            # Grant privileges
            print(f"\nGranting privileges to '{db_user}'...")
            cursor.execute("GRANT ALL PRIVILEGES ON ecommerce_db.* TO 'ecommerce_user'@'localhost'")
            cursor.execute("FLUSH PRIVILEGES")
            print(f"✅ Privileges granted successfully!")
            
            # Test connection with new user
            print(f"\nTesting connection with new user...")
            test_connection = mysql.connector.connect(
                host="localhost",
                user=db_user,
                password=db_password,
                database="ecommerce_db",
                port=3306
            )
            
            if test_connection.is_connected():
                print("✅ Connection test successful!")
                test_connection.close()
                
                # Show user privileges
                cursor.execute("SHOW GRANTS FOR 'ecommerce_user'@'localhost'")
                privileges = cursor.fetchall()
                print(f"\nUser privileges:")
                for priv in privileges:
                    print(f"  {priv[0]}")
                
                return True
            else:
                print("❌ Connection test failed!")
                return False
            
        else:
            print("❌ Failed to connect to MySQL")
            return False
            
    except Error as e:
        print(f"❌ Error: {e}")
        return False
        
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

def test_database_operations():
    """Test basic database operations."""
    print("\n=== Testing Database Operations ===")
    
    # Get credentials
    db_user = input("Enter database user (default: root): ").strip() or "root"
    db_password = getpass.getpass(f"Enter password for '{db_user}': ")
    
    try:
        # Connect to database
        connection = mysql.connector.connect(
            host="localhost",
            user=db_user,
            password=db_password,
            database="ecommerce_db",
            port=3306
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Test basic operations
            print("\nTesting basic operations...")
            
            # Test SELECT
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"✅ MySQL version: {version[0]}")
            
            # Test CREATE TABLE
            test_table = "test_table"
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {test_table} (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(50))")
            print(f"✅ Table '{test_table}' created/verified")
            
            # Test INSERT
            cursor.execute(f"INSERT INTO {test_table} (name) VALUES ('test')")
            print(f"✅ Insert operation successful")
            
            # Test SELECT
            cursor.execute(f"SELECT * FROM {test_table}")
            result = cursor.fetchone()
            print(f"✅ Select operation successful: {result}")
            
            # Test UPDATE
            cursor.execute(f"UPDATE {test_table} SET name = 'updated' WHERE id = 1")
            print(f"✅ Update operation successful")
            
            # Test DELETE
            cursor.execute(f"DELETE FROM {test_table} WHERE id = 1")
            print(f"✅ Delete operation successful")
            
            # Clean up test table
            cursor.execute(f"DROP TABLE {test_table}")
            print(f"✅ Test table cleaned up")
            
            print("\n🎉 All database operations tested successfully!")
            return True
            
        else:
            print("❌ Failed to connect to database")
            return False
            
    except Error as e:
        print(f"❌ Error: {e}")
        return False
        
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

def main():
    """Main function."""
    print("🗄️  Database Setup for Django E-commerce API")
    print("=" * 50)
    
    # Step 1: Create database
    if not create_database():
        print("❌ Database creation failed")
        return
    
    # Step 2: Create dedicated user
    if not create_dedicated_user():
        print("❌ User creation failed")
        return
    
    # Step 3: Test database operations
    if not test_database_operations():
        print("❌ Database operations test failed")
        return
    
    print("\n🎉 Database setup completed successfully!")
    print("\n=== Your database is ready! ===")
    print("Database: ecommerce_db")
    print("User: ecommerce_user")
    print("Host: localhost")
    print("Port: 3306")
    
    print("\n=== Next Steps ===")
    print("1. Your .env file will be created automatically")
    print("2. Run: python manage.py migrate")
    print("3. Run: python manage.py runserver")
    
    print("\n=== For Railway Deployment ===")
    print("Your project is fully prepared for Railway deployment!")
    print("Follow the guide in: HOW_TO_DEPLOY_ON_RAILWAY.md")

if __name__ == "__main__":
    main()
