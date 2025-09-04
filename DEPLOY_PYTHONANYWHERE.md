# 🚀 PythonAnywhere Deployment Guide

This guide will walk you through deploying your Django E-commerce API on PythonAnywhere.

## 📋 Prerequisites

- PythonAnywhere account (free or paid)
- Git repository access
- Basic knowledge of command line operations

## 🔧 Step 1: PythonAnywhere Setup

### 1.1 Create Account
- Go to [PythonAnywhere.com](https://www.pythonanywhere.com)
- Sign up for a free account or upgrade to paid for more features

### 1.2 Access Your Dashboard
- Log in to your PythonAnywhere dashboard
- Note your username (you'll need this for configuration)

## 📥 Step 2: Clone Your Repository

### 2.1 Open Bash Console
- In your PythonAnywhere dashboard, click on "Bash" console
- This opens a Linux terminal where you can run commands

### 2.2 Clone Repository
```bash
# Navigate to your home directory
cd ~

# Clone your repository
git clone https://github.com/zeyad-houssainy/alx-BE-graduation-project-ECommerce.git

# Navigate into the project directory
cd alx-BE-graduation-project-ECommerce
```

## 🗄️ Step 3: Database Setup

### 3.1 Create MySQL Database
- In your PythonAnywhere dashboard, go to "Databases" tab
- Create a new MySQL database
- Note the database name, username, and password

### 3.2 Database Configuration
Your database details will look like:
- **Database Name**: `yourusername$ecommerce_db`
- **Host**: `yourusername.mysql.pythonanywhere-services.com`
- **Username**: `yourusername`
- **Password**: `your-chosen-password`

## ⚙️ Step 4: Environment Configuration

### 4.1 Create Environment File
```bash
# Copy the example environment file
cp pythonanywhere.env.example .env

# Edit the .env file with your actual values
nano .env
```

### 4.2 Update Environment Variables
Replace the placeholder values in `.env`:
```bash
SECRET_KEY=your-actual-secret-key
DEBUG=False
ALLOWED_HOSTS=yourusername.pythonanywhere.com
DB_NAME=yourusername$ecommerce_db
DB_HOST=yourusername.mysql.pythonanywhere-services.com
DB_USER=yourusername
DB_PASSWORD=your-actual-database-password
DB_PORT=3306
JWT_SECRET_KEY=your-actual-jwt-secret
CORS_ALLOWED_ORIGINS=https://yourusername.pythonanywhere.com
```

### 4.3 Generate Secret Keys
```bash
# Generate Django secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Generate JWT secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## 📦 Step 5: Install Dependencies

### 5.1 Install Python Packages
```bash
# Install PythonAnywhere-optimized packages
pip install --user -r requirements.txt
```

### 5.2 Verify Installation
```bash
# Check if Django is installed
python -c "import django; print(django.get_version())"
```

## 🗄️ Step 6: Database Migration

### 6.1 Run Migrations
```bash
# Apply database migrations
python manage.py migrate
```

### 6.2 Create Superuser
```bash
# Create admin user
python manage.py createsuperuser
```

## 📁 Step 7: Static Files

### 7.1 Collect Static Files
```bash
# Collect all static files
python manage.py collectstatic --noinput
```

## 🌐 Step 8: Web App Configuration

### 8.1 Create Web App
- In your PythonAnywhere dashboard, go to "Web" tab
- Click "Add a new web app"
- Choose "Manual configuration"
- Select Python version (3.9 or higher recommended)

### 8.2 Configure WSGI File
- Click on your web app
- In the "Code" section, click on the WSGI configuration file
- Replace the content with the path to your `pythonanywhere_wsgi.py` file
- Update the username in the path: `/home/yourusername/alx-BE-graduation-project-ECommerce/pythonanywhere_wsgi.py`

### 8.3 Set Environment Variables
- In the "Environment variables" section, add:
  - `PYTHONPATH`: `/home/yourusername/alx-BE-graduation-project-ECommerce`
  - `DJANGO_SETTINGS_MODULE`: `ecommerce_api.settings`

### 8.4 Configure Static Files
- In the "Static files" section:
  - **URL**: `/static/`
  - **Directory**: `/home/yourusername/alx-BE-graduation-project-ECommerce/staticfiles`

## 🔄 Step 9: Reload and Test

### 9.1 Reload Web App
- Click the "Reload" button for your web app
- Wait for the reload to complete

### 9.2 Test Your API
- Visit your web app URL: `https://yourusername.pythonanywhere.com`
- Test the API endpoints: `https://yourusername.pythonanywhere.com/api/`
- Check admin panel: `https://yourusername.pythonanywhere.com/admin/`

## 🚨 Step 10: Troubleshooting

### Common Issues and Solutions

#### 1. Import Errors
```bash
# Check Python path
python -c "import sys; print(sys.path)"

# Verify Django installation
python -c "import django; print(django.__file__)"
```

#### 2. Database Connection Issues
```bash
# Test database connection
python manage.py dbshell

# Check database settings
python manage.py check --database default
```

#### 3. Static Files Not Loading
```bash
# Recollect static files
python manage.py collectstatic --noinput --clear

# Check static files directory
ls -la staticfiles/
```

#### 4. Permission Issues
```bash
# Check file permissions
ls -la

# Fix permissions if needed
chmod 755 staticfiles/
chmod 755 media/
```

## 📊 Step 11: Monitoring and Maintenance

### 11.1 Check Logs
- In your web app dashboard, check error logs
- Monitor for any issues or errors

### 11.2 Regular Updates
```bash
# Pull latest changes
git pull origin main

# Install new dependencies
pip install --user -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Reload web app
```

## 🔒 Step 12: Security Considerations

### 12.1 Production Settings
- Ensure `DEBUG=False` in production
- Use strong secret keys
- Enable HTTPS (automatic on PythonAnywhere)

### 12.2 Database Security
- Use strong database passwords
- Regularly backup your database
- Monitor database access

## 🎉 Congratulations!

Your Django E-commerce API is now deployed on PythonAnywhere!

### Your API Endpoints:
- **Home Page**: `https://yourusername.pythonanywhere.com/`
- **API Root**: `https://yourusername.pythonanywhere.com/api/`
- **Admin Panel**: `https://yourusername.pythonanywhere.com/admin/`
- **Products**: `https://yourusername.pythonanywhere.com/api/products/`
- **Categories**: `https://yourusername.pythonanywhere.com/api/categories/`
- **Users**: `https://yourusername.pythonanywhere.com/api/users/`

### Next Steps:
1. Test all API endpoints
2. Create some test data using your mock data buttons
3. Set up monitoring and logging
4. Consider setting up automated backups
5. Monitor performance and optimize as needed

## 📞 Support

If you encounter any issues:
1. Check the PythonAnywhere error logs
2. Review this deployment guide
3. Check Django documentation
4. Use the troubleshooting section above

Happy coding! 🚀
