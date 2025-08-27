# MySQL Setup Guide for Local Development

This guide will help you set up MySQL for your Django E-commerce API project.

## Prerequisites

- MySQL Server installed and running
- Python 3.11+
- pip package manager

## Quick Setup (Recommended)

### Option 1: Automated Setup
Run the automated setup script:
```bash
# Windows
setup_local.bat

# Or manually run the Python script
python setup_mysql.py
```

### Option 2: Manual Setup
Follow the steps below if you prefer manual setup.

## Manual MySQL Setup

### Step 1: Install MySQL Server

#### Windows
1. Download MySQL Installer from [MySQL Downloads](https://dev.mysql.com/downloads/installer/)
2. Run the installer and follow the setup wizard
3. Choose "Developer Default" or "Server only" installation
4. Set a root password when prompted
5. Complete the installation

#### macOS
```bash
# Using Homebrew
brew install mysql

# Start MySQL service
brew services start mysql
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install mysql-server

# Start MySQL service
sudo systemctl start mysql
sudo systemctl enable mysql
```

### Step 2: Create Database and User

1. **Connect to MySQL as root:**
   ```bash
   mysql -u root -p
   ```

2. **Create the database:**
   ```sql
   CREATE DATABASE ecommerce_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

3. **Create a dedicated user:**
   ```sql
   CREATE USER 'ecommerce_user'@'localhost' IDENTIFIED BY 'your_secure_password';
   ```

4. **Grant privileges:**
   ```sql
   GRANT ALL PRIVILEGES ON ecommerce_db.* TO 'ecommerce_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

5. **Exit MySQL:**
   ```sql
   EXIT;
   ```

### Step 3: Configure Environment Variables

1. **Copy the environment template:**
   ```bash
   copy env.example .env
   ```

2. **Edit `.env` file with your database credentials:**
   ```bash
   # MySQL Database Configuration
   DB_NAME=ecommerce_db
   DB_HOST=localhost
   DB_USER=ecommerce_user
   DB_PASSWORD=your_secure_password
   DB_PORT=3306
   ```

### Step 4: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Run Database Migrations

```bash
python manage.py migrate
```

### Step 6: Create Superuser

```bash
python manage.py createsuperuser
```

### Step 7: Start Development Server

```bash
python manage.py runserver
```

## Troubleshooting

### Common Issues

#### 1. "Access denied for user 'root'@'localhost'"
- **Solution**: Make sure you're using the correct root password
- **Alternative**: Reset MySQL root password if needed

#### 2. "Can't connect to MySQL server"
- **Solution**: Ensure MySQL service is running
- **Windows**: Check Services app for MySQL
- **macOS**: `brew services start mysql`
- **Linux**: `sudo systemctl start mysql`

#### 3. "Unknown database 'ecommerce_db'"
- **Solution**: Create the database first using the SQL commands above

#### 4. "Authentication plugin 'caching_sha2_password' cannot be loaded"
- **Solution**: Use PyMySQL instead of mysql-connector-python
- **Alternative**: Change MySQL user authentication method

### Reset MySQL Root Password

#### Windows
1. Stop MySQL service
2. Start MySQL with `--skip-grant-tables`
3. Connect and update password
4. Restart MySQL service

#### macOS/Linux
```bash
sudo mysqld_safe --skip-grant-tables &
mysql -u root
UPDATE mysql.user SET authentication_string=PASSWORD('new_password') WHERE User='root';
FLUSH PRIVILEGES;
EXIT;
sudo killall mysqld
sudo systemctl start mysql
```

## Database Configuration

### Connection Parameters
- **Host**: localhost (or 127.0.0.1)
- **Port**: 3306 (default MySQL port)
- **Database**: ecommerce_db
- **User**: ecommerce_user (or root)
- **Charset**: utf8mb4

### Security Best Practices
1. **Don't use root user** for application connections
2. **Use strong passwords** for database users
3. **Limit user privileges** to only necessary databases
4. **Keep MySQL updated** with security patches

## Testing Connection

### Test with Python
```python
import mysql.connector

try:
    connection = mysql.connector.connect(
        host="localhost",
        user="ecommerce_user",
        password="your_password",
        database="ecommerce_db"
    )
    if connection.is_connected():
        print("✅ MySQL connection successful!")
        connection.close()
except Error as e:
    print(f"❌ Error: {e}")
```

### Test with MySQL Client
```bash
mysql -u ecommerce_user -p ecommerce_db
```

## Next Steps

After successful MySQL setup:

1. **Run migrations**: `python manage.py migrate`
2. **Create superuser**: `python manage.py createsuperuser`
3. **Start development server**: `python manage.py runserver`
4. **Test API endpoints**: Visit http://localhost:8000/api/
5. **Access admin**: Visit http://localhost:8000/admin/

## Support

If you encounter issues:

1. Check MySQL error logs
2. Verify service status
3. Test connection manually
4. Review Django settings
5. Check environment variables

---

**Note**: This setup is for local development only. For production deployment on Railway, the database configuration will be handled automatically by Railway's MySQL service.
