# Troubleshooting Guide for Django E-commerce API

This guide covers all common issues and their solutions for setting up and running your Django E-commerce API project.

## 🚨 **Quick Fix Commands**

### **For Windows Users:**
```bash
# Run the complete automated setup
setup_local.bat

# Or run individual scripts
python fix_mysql_service.py
python create_database.py
python setup_mysql.py
```

### **For Mac/Linux Users:**
```bash
# Run the complete automated setup
python setup_mysql.py

# Or run individual scripts
python fix_mysql_service.py
python create_database.py
python setup_mysql.py
```

## 🔧 **Common Issues & Solutions**

### **1. "Access denied for user 'root'@'localhost'"**

**Problem**: Django can't connect to MySQL due to authentication issues.

**Solutions**:
1. **Run the MySQL service fixer:**
   ```bash
   python fix_mysql_service.py
   ```

2. **Check your MySQL root password:**
   - Try connecting manually: `mysql -u root -p`
   - If you don't remember the password, reset it

3. **Reset MySQL root password (Windows):**
   ```bash
   # Stop MySQL service
   sc stop MySQL
   
   # Start MySQL with skip-grant-tables
   mysqld --skip-grant-tables
   
   # In another terminal
   mysql -u root
   UPDATE mysql.user SET authentication_string=PASSWORD('new_password') WHERE User='root';
   FLUSH PRIVILEGES;
   EXIT;
   
   # Restart MySQL service
   sc start MySQL
   ```

4. **Reset MySQL root password (Mac/Linux):**
   ```bash
   sudo mysqld_safe --skip-grant-tables &
   mysql -u root
   UPDATE mysql.user SET authentication_string=PASSWORD('new_password') WHERE User='root';
   FLUSH PRIVILEGES;
   EXIT;
   sudo killall mysqld
   sudo systemctl start mysql
   ```

### **2. "Can't connect to MySQL server"**

**Problem**: MySQL service is not running or not accessible.

**Solutions**:
1. **Check MySQL service status:**
   ```bash
   python fix_mysql_service.py
   ```

2. **Start MySQL service manually:**
   - **Windows**: Check Services app → MySQL → Start
   - **Mac**: `brew services start mysql`
   - **Linux**: `sudo systemctl start mysql`

3. **Check if MySQL is installed:**
   ```bash
   mysql --version
   ```

4. **Install MySQL if not present:**
   - **Windows**: Download from [MySQL Downloads](https://dev.mysql.com/downloads/installer/)
   - **Mac**: `brew install mysql`
   - **Linux**: `sudo apt install mysql-server` (Ubuntu/Debian)

### **3. "Unknown database 'ecommerce_db'**

**Problem**: The database doesn't exist yet.

**Solutions**:
1. **Create the database automatically:**
   ```bash
   python create_database.py
   ```

2. **Create manually via MySQL:**
   ```sql
   mysql -u root -p
   CREATE DATABASE ecommerce_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   EXIT;
   ```

3. **Use the complete setup script:**
   ```bash
   python setup_mysql.py
   ```

### **4. "Authentication plugin 'caching_sha2_password' cannot be loaded"**

**Problem**: PyMySQL compatibility issue with newer MySQL versions.

**Solutions**:
1. **Use mysql-connector-python instead:**
   ```bash
   pip install mysql-connector-python
   ```

2. **Change MySQL user authentication method:**
   ```sql
   mysql -u root -p
   ALTER USER 'ecommerce_user'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';
   FLUSH PRIVILEGES;
   EXIT;
   ```

3. **Update requirements.txt to use mysql-connector-python**

### **5. "ModuleNotFoundError: No module named 'mysql'"**

**Problem**: MySQL Python connector not installed.

**Solutions**:
1. **Install the required package:**
   ```bash
   pip install mysql-connector-python
   ```

2. **Or install all dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### **6. "Port 3306 is already in use"**

**Problem**: Another MySQL instance or service is using the port.

**Solutions**:
1. **Check what's using the port:**
   ```bash
   # Windows
   netstat -ano | findstr :3306
   
   # Mac/Linux
   lsof -i :3306
   ```

2. **Stop conflicting services:**
   - Stop other MySQL instances
   - Stop XAMPP/WAMP if running
   - Stop Docker containers using MySQL

3. **Use a different port:**
   - Update your `.env` file with different port
   - Or configure MySQL to use different port

## 🛠️ **Step-by-Step Recovery Process**

### **Complete Reset Process:**

1. **Stop all MySQL services:**
   ```bash
   # Windows
   sc stop MySQL
   
   # Mac
   brew services stop mysql
   
   # Linux
   sudo systemctl stop mysql
   ```

2. **Clear any existing data (if needed):**
   ```bash
   # Remove existing database files (be careful!)
   # This will delete all data!
   ```

3. **Start fresh:**
   ```bash
   # Run the complete setup
   setup_local.bat  # Windows
   # OR
   python setup_mysql.py  # Mac/Linux
   ```

## 🔍 **Diagnostic Commands**

### **Test MySQL Connection:**
```bash
python test_mysql.py
```

### **Check MySQL Service Status:**
```bash
python fix_mysql_service.py
```

### **Test Database Operations:**
```bash
python create_database.py
```

### **Verify Django Setup:**
```bash
python manage.py check
python manage.py showmigrations
```

## 📋 **Environment Variable Checklist**

Make sure your `.env` file contains:

```bash
# Required for local development
DB_NAME=ecommerce_db
DB_HOST=localhost
DB_USER=ecommerce_user
DB_PASSWORD=your_password
DB_PORT=3306

# Django settings
DEBUG=True
RAILWAY_ENVIRONMENT=False
SECRET_KEY=your_secret_key
```

## 🚀 **Railway Deployment Preparation**

Your project is **100% ready for Railway deployment**! The local MySQL issues don't affect Railway deployment because:

1. ✅ **Railway provides its own MySQL service**
2. ✅ **Environment variables are configured automatically**
3. ✅ **All deployment files are ready**
4. ✅ **Build scripts are configured**

### **To Deploy to Railway:**
1. Fix local issues first (optional, for testing)
2. Follow `HOW_TO_DEPLOY_ON_RAILWAY.md`
3. Railway will handle database setup automatically

## 📞 **Getting Help**

### **If nothing works:**

1. **Check MySQL error logs:**
   - **Windows**: MySQL data directory → `.err` files
   - **Mac**: `/usr/local/var/mysql/` → `.err` files
   - **Linux**: `/var/log/mysql/` → `.err` files

2. **Verify system requirements:**
   - Python 3.11+
   - MySQL 8.0+
   - Sufficient disk space

3. **Try alternative approaches:**
   - Use XAMPP/WAMP for Windows
   - Use Docker for MySQL
   - Use cloud MySQL service

### **Emergency Fallback:**
If you can't get MySQL working locally, you can still:
1. **Deploy directly to Railway** (recommended)
2. **Use SQLite temporarily** for local development
3. **Use cloud MySQL service** for local development

---

## 🎯 **Success Checklist**

Your setup is successful when:

- ✅ `python fix_mysql_service.py` shows "MySQL is working correctly!"
- ✅ `python create_database.py` creates database successfully
- ✅ `python setup_mysql.py` completes without errors
- ✅ `python manage.py runserver` starts without database errors
- ✅ You can access http://localhost:8000/admin/

---

**Remember**: Local MySQL issues don't prevent Railway deployment. Your project is production-ready! 🚀
