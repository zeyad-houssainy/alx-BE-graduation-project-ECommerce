#!/usr/bin/env python3
"""
MySQL Service Fixer Script
This script helps diagnose and fix MySQL service issues.
"""

import subprocess
import sys
import os
import platform
import time

def get_os_info():
    """Get operating system information."""
    system = platform.system().lower()
    if system == "windows":
        return "windows"
    elif system == "darwin":
        return "macos"
    elif system == "linux":
        return "linux"
    else:
        return "unknown"

def check_mysql_installation():
    """Check if MySQL is installed."""
    print("=== Checking MySQL Installation ===")
    
    os_type = get_os_info()
    
    if os_type == "windows":
        # Check if MySQL is in PATH
        try:
            result = subprocess.run(["mysql", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ MySQL is installed and accessible")
                return True
        except FileNotFoundError:
            pass
        
        # Check if MySQL service exists
        try:
            result = subprocess.run(["sc", "query", "MySQL"], capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ MySQL service exists")
                return True
        except:
            pass
        
        print("❌ MySQL is not installed or not in PATH")
        print("Please install MySQL from: https://dev.mysql.com/downloads/installer/")
        return False
        
    elif os_type == "macos":
        try:
            result = subprocess.run(["brew", "list", "mysql"], capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ MySQL is installed via Homebrew")
                return True
        except:
            pass
        
        try:
            result = subprocess.run(["mysql", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ MySQL is installed and accessible")
                return True
        except:
            pass
        
        print("❌ MySQL is not installed")
        print("Install with: brew install mysql")
        return False
        
    elif os_type == "linux":
        try:
            result = subprocess.run(["which", "mysql"], capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ MySQL is installed")
                return True
        except:
            pass
        
        print("❌ MySQL is not installed")
        print("Install with: sudo apt install mysql-server (Ubuntu/Debian)")
        print("Or: sudo yum install mysql-server (CentOS/RHEL)")
        return False
    
    return False

def check_mysql_service_status():
    """Check MySQL service status."""
    print("\n=== Checking MySQL Service Status ===")
    
    os_type = get_os_info()
    
    if os_type == "windows":
        try:
            result = subprocess.run(["sc", "query", "MySQL"], capture_output=True, text=True)
            if result.returncode == 0:
                if "RUNNING" in result.stdout:
                    print("✅ MySQL service is running")
                    return True
                elif "STOPPED" in result.stdout:
                    print("⚠️  MySQL service is stopped")
                    return False
                else:
                    print("ℹ️  MySQL service status unknown")
                    return False
        except:
            print("❌ Could not check MySQL service status")
            return False
            
    elif os_type == "macos":
        try:
            result = subprocess.run(["brew", "services", "list"], capture_output=True, text=True)
            if result.returncode == 0:
                if "mysql" in result.stdout and "started" in result.stdout:
                    print("✅ MySQL service is running")
                    return True
                else:
                    print("⚠️  MySQL service is not running")
                    return False
        except:
            print("❌ Could not check MySQL service status")
            return False
            
    elif os_type == "linux":
        try:
            result = subprocess.run(["systemctl", "is-active", "mysql"], capture_output=True, text=True)
            if result.returncode == 0 and "active" in result.stdout:
                print("✅ MySQL service is running")
                return True
            else:
                print("⚠️  MySQL service is not running")
                return False
        except:
            print("❌ Could not check MySQL service status")
            return False
    
    return False

def start_mysql_service():
    """Start MySQL service."""
    print("\n=== Starting MySQL Service ===")
    
    os_type = get_os_info()
    
    if os_type == "windows":
        try:
            print("Starting MySQL service...")
            result = subprocess.run(["sc", "start", "MySQL"], capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ MySQL service started successfully")
                return True
            else:
                print(f"❌ Failed to start MySQL service: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ Error starting MySQL service: {e}")
            return False
            
    elif os_type == "macos":
        try:
            print("Starting MySQL service...")
            result = subprocess.run(["brew", "services", "start", "mysql"], capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ MySQL service started successfully")
                return True
            else:
                print(f"❌ Failed to start MySQL service: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ Error starting MySQL service: {e}")
            return False
            
    elif os_type == "linux":
        try:
            print("Starting MySQL service...")
            result = subprocess.run(["sudo", "systemctl", "start", "mysql"], capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ MySQL service started successfully")
                return True
            else:
                print(f"❌ Failed to start MySQL service: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ Error starting MySQL service: {e}")
            return False
    
    return False

def test_mysql_connection():
    """Test MySQL connection."""
    print("\n=== Testing MySQL Connection ===")
    
    try:
        import mysql.connector
        
        # Try common connection methods
        connection_methods = [
            {"host": "localhost", "user": "root", "password": ""},
            {"host": "localhost", "user": "root", "password": "root"},
            {"host": "localhost", "user": "root", "password": "password"},
            {"host": "127.0.0.1", "user": "root", "password": ""},
            {"host": "127.0.0.1", "user": "root", "password": "root"},
        ]
        
        for method in connection_methods:
            try:
                print(f"Trying: {method['user']}@{method['host']} (password: {'*' * len(method['password']) if method['password'] else 'none'})")
                connection = mysql.connector.connect(**method, port=3306)
                if connection.is_connected():
                    print(f"✅ Successfully connected with: {method['user']}@{method['host']}")
                    connection.close()
                    return True
            except Exception as e:
                print(f"❌ Failed: {str(e)[:100]}...")
                continue
        
        print("❌ All connection attempts failed")
        return False
        
    except ImportError:
        print("❌ mysql-connector-python not installed")
        print("Install with: pip install mysql-connector-python")
        return False

def fix_mysql_issues():
    """Main function to fix MySQL issues."""
    print("🔧 MySQL Service Fixer")
    print("=" * 40)
    
    # Step 1: Check installation
    if not check_mysql_installation():
        print("\n❌ Please install MySQL first")
        return False
    
    # Step 2: Check service status
    if not check_mysql_service_status():
        print("\n⚠️  MySQL service is not running")
        
        # Ask user if they want to start it
        response = input("\nWould you like to start MySQL service? (y/n): ").lower().strip()
        if response == 'y':
            if start_mysql_service():
                print("Waiting for service to fully start...")
                time.sleep(5)  # Wait for service to fully start
            else:
                print("❌ Failed to start MySQL service")
                return False
        else:
            print("Please start MySQL service manually")
            return False
    
    # Step 3: Test connection
    if not test_mysql_connection():
        print("\n❌ MySQL connection failed even though service is running")
        print("This might be an authentication issue")
        return False
    
    print("\n🎉 MySQL is working correctly!")
    return True

def main():
    """Main function."""
    try:
        success = fix_mysql_issues()
        if success:
            print("\n✅ MySQL issues resolved!")
            print("\nNext steps:")
            print("1. Run: python setup_mysql.py")
            print("2. Or run: setup_local.bat")
        else:
            print("\n❌ Could not resolve MySQL issues")
            print("\nManual troubleshooting:")
            print("1. Check if MySQL is installed correctly")
            print("2. Ensure MySQL service is running")
            print("3. Verify firewall settings")
            print("4. Check MySQL error logs")
    except KeyboardInterrupt:
        print("\n\nSetup interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
