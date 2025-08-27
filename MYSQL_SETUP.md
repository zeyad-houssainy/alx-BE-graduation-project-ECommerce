# MySQL Database Setup Guide

This guide will help you set up MySQL for your Django e-commerce project.

## 🗄️ Prerequisites

- MySQL 8.0+ server installed
- MySQL client tools
- Python 3.11+ with pip
- Virtual environment activated

## 📋 Step-by-Step Setup

### 1. Install MySQL Server

#### On Windows:
```bash
# Download MySQL Installer from official website
# https://dev.mysql.com/downloads/installer/
# Run the installer and follow the setup wizard
```

#### On macOS:
```bash
# Using Homebrew
brew install mysql

# Start MySQL service
brew services start mysql
```

#### On Ubuntu/Debian:
```bash
# Update package list
sudo apt update

# Install MySQL server
sudo apt install mysql-server

# Start MySQL service
sudo systemctl start mysql
sudo systemctl enable mysql
```

### 2. Secure MySQL Installation

```bash
# Run security script
sudo mysql_secure_installation

# Follow the prompts:
# - Set root password
# - Remove anonymous users
# - Disallow root login remotely
# - Remove test database
# - Reload privilege tables
```

### 3. Access MySQL as Root

```bash
# Connect to MySQL as root
mysql -u root -p

# Enter your root password when prompted
```

### 4. Create Database and User

```sql
-- Create the database
CREATE DATABASE ecommerce_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create a dedicated user (recommended for production)
CREATE USER 'ecommerce_user'@'localhost' IDENTIFIED BY 'your_secure_password';

-- Grant privileges to the user
GRANT ALL PRIVILEGES ON ecommerce_db.* TO 'ecommerce_user'@'localhost';

-- Grant additional privileges for Django
GRANT CREATE, ALTER, DROP, INDEX, REFERENCES ON ecommerce_db.* TO 'ecommerce_user'@'localhost';

-- Flush privileges
FLUSH PRIVILEGES;

-- Verify the database was created
SHOW DATABASES;

-- Exit MySQL
EXIT;
```

### 5. Test Database Connection

```bash
# Test connection with the new user
mysql -u ecommerce_user -p ecommerce_db

# You should see the MySQL prompt
mysql>

# Exit
EXIT;
```

## 🔧 Django Configuration

### 1. Install MySQL Client for Python

```bash
# Activate your virtual environment first
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install mysqlclient
pip install mysqlclient

# If you encounter issues, try:
pip install --only-binary=all mysqlclient
```

### 2. Create Environment File

```bash
# Copy the example environment file
cp env_example.txt .env

# Edit the .env file with your MySQL credentials
nano .env  # or use your preferred editor
```

Update the `.env` file with your MySQL settings:
```env
# Django Settings
SECRET_KEY=django-insecure-s8md8r=z3^2w8aud0buw4bvpe1uy%l#n=p30it8ozh7981cp47
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# MySQL Database Configuration
DB_NAME=ecommerce_db
DB_USER=ecommerce_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=3306

# JWT Settings
JWT_SECRET_KEY=your-jwt-secret-key-here
JWT_ACCESS_TOKEN_LIFETIME=1
JWT_REFRESH_TOKEN_LIFETIME=7

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://localhost:8080,http://127.0.0.1:8080
```

### 3. Verify Django Settings

Ensure your `settings.py` has the correct database configuration:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME', default='ecommerce_db'),
        'USER': config('DB_USER', default='root'),
        'PASSWORD': config('DB_PASSWORD', default=''),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
```

## 🚀 Database Operations

### 1. Run Django Migrations

```bash
# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Verify tables were created
python manage.py showmigrations
```

### 2. Create Superuser

```bash
python manage.py createsuperuser
# Follow the prompts to create admin user
```

### 3. Test Database Connection

```bash
# Check Django configuration
python manage.py check

# Test database connection
python manage.py dbshell
```

## 🔍 Troubleshooting

### Common Issues and Solutions

#### 1. "mysqlclient not found" Error
```bash
# Install system dependencies first
# On Ubuntu/Debian:
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential

# On macOS:
brew install mysql-connector-c

# Then reinstall mysqlclient
pip uninstall mysqlclient
pip install mysqlclient
```

#### 2. "Access denied for user" Error
```sql
-- Connect as root and check user privileges
mysql -u root -p

-- Check if user exists
SELECT User, Host FROM mysql.user WHERE User = 'ecommerce_user';

-- If user doesn't exist, recreate it
DROP USER IF EXISTS 'ecommerce_user'@'localhost';
CREATE USER 'ecommerce_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON ecommerce_db.* TO 'ecommerce_user'@'localhost';
FLUSH PRIVILEGES;
```

#### 3. "Can't connect to MySQL server" Error
```bash
# Check if MySQL is running
sudo systemctl status mysql  # On Linux
brew services list           # On macOS

# Start MySQL if not running
sudo systemctl start mysql  # On Linux
brew services start mysql   # On macOS
```

#### 4. Character Set Issues
```sql
-- Connect to MySQL and check character set
mysql -u root -p

-- Check current character set
SHOW VARIABLES LIKE 'character_set%';

-- Set proper character set
SET GLOBAL character_set_server = 'utf8mb4';
SET GLOBAL collation_server = 'utf8mb4_unicode_ci';
```

## 📊 Database Management

### Useful MySQL Commands

```sql
-- Connect to database
mysql -u ecommerce_user -p ecommerce_db

-- Show all tables
SHOW TABLES;

-- Describe table structure
DESCRIBE products_product;

-- Check table data
SELECT * FROM products_product LIMIT 5;

-- Check database size
SELECT 
    table_schema AS 'Database',
    ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS 'Size (MB)'
FROM information_schema.tables 
WHERE table_schema = 'ecommerce_db'
GROUP BY table_schema;
```

### Backup and Restore

#### Backup Database
```bash
# Create backup
mysqldump -u ecommerce_user -p ecommerce_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Compress backup
gzip backup_$(date +%Y%m%d_%H%M%S).sql
```

#### Restore Database
```bash
# Restore from backup
mysql -u ecommerce_user -p ecommerce_db < backup_file.sql

# If compressed
gunzip < backup_file.sql.gz | mysql -u ecommerce_user -p ecommerce_db
```

## 🔒 Security Best Practices

### 1. User Privileges
- Use dedicated database user, not root
- Grant only necessary privileges
- Use strong passwords

### 2. Network Security
- Bind MySQL to localhost only
- Use firewall rules if external access needed
- Enable SSL for remote connections

### 3. Regular Maintenance
- Regular backups
- Monitor database performance
- Keep MySQL updated

## 📈 Performance Optimization

### 1. MySQL Configuration
```ini
# Add to /etc/mysql/mysql.conf.d/mysqld.cnf
[mysqld]
# Buffer pool size (adjust based on available RAM)
innodb_buffer_pool_size = 1G

# Query cache
query_cache_type = 1
query_cache_size = 64M

# Connection handling
max_connections = 200
```

### 2. Django Optimization
```python
# In settings.py
DATABASES = {
    'default': {
        # ... existing config ...
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'autocommit': True,
        },
        'CONN_MAX_AGE': 60,  # Persistent connections
    }
}
```

## ✅ Verification Checklist

- [ ] MySQL server installed and running
- [ ] Database `ecommerce_db` created
- [ ] User `ecommerce_user` created with proper privileges
- [ ] Python `mysqlclient` package installed
- [ ] `.env` file configured with correct credentials
- [ ] Django migrations run successfully
- [ ] Superuser created
- [ ] Admin interface accessible
- [ ] API endpoints responding correctly

## 🆘 Getting Help

If you encounter issues:

1. Check MySQL error logs: `/var/log/mysql/error.log`
2. Verify Django settings with `python manage.py check`
3. Test database connection manually
4. Check MySQL user privileges
5. Ensure MySQL service is running

## 📚 Additional Resources

- [MySQL 8.0 Reference Manual](https://dev.mysql.com/doc/refman/8.0/en/)
- [Django Database Documentation](https://docs.djangoproject.com/en/stable/ref/databases/)
- [MySQL Python Connector](https://dev.mysql.com/doc/connector-python/en/)

---

**Note**: This guide assumes MySQL 8.0+. For older versions, some commands may differ.






