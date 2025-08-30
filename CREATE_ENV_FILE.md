# 🔧 Fix 2: Create .env File

## 📋 **Step-by-Step Instructions**

### **Step 1: Access Your PythonAnywhere Files**
1. Go to your PythonAnywhere dashboard
2. Click on **"Files"** tab
3. Navigate to: `/home/zeyadhoussainy/alx-BE-graduation-project-ECommerce/`

### **Step 2: Create the .env File**
1. Click **"New file"** button
2. Name it exactly: `.env` (with the dot at the beginning)
3. Click **"Create"**

### **Step 3: Copy the Environment Variables**
Copy and paste this content into your `.env` file:

```bash
# PythonAnywhere Environment Variables
# Production configuration for zeyadhoussainy.pythonanywhere.com

# Django Settings
SECRET_KEY=django-insecure-production-key-change-this-immediately
DEBUG=False
ALLOWED_HOSTS=*
PYTHONANYWHERE_ENVIRONMENT=True

# Database Configuration (PythonAnywhere MySQL)
DB_NAME=zeyadhoussainy$ecommerce_db
DB_HOST=zeyadhoussainy.mysql.pythonanywhere-services.com
DB_USER=zeyadhoussainy
DB_PASSWORD=your-database-password-here
DB_PORT=3306

# JWT Authentication
JWT_SECRET_KEY=your-jwt-secret-key-change-this-immediately

# CORS Settings
CORS_ALLOWED_ORIGINS=https://zeyadhoussainy.pythonanywhere.com

# Security Settings (Production)
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_SSL_REDIRECT=True

# Static and Media Files
STATIC_ROOT=/home/zeyadhoussainy/alx-BE-graduation-project-ECommerce/staticfiles
MEDIA_ROOT=/home/zeyadhoussainy/alx-BE-graduation-project-ECommerce/media

# Logging
LOG_LEVEL=INFO
```

### **Step 4: Save the File**
1. Click **"Save"** button
2. Verify the file was created successfully

## ⚠️ **IMPORTANT: Update These Values**

### **1. Database Password**
```bash
DB_PASSWORD=your-actual-mysql-password-here
```
- Replace `your-database-password-here` with your actual MySQL password from PythonAnywhere

### **2. Generate New Secret Keys**
Run these commands in your PythonAnywhere bash console:

```bash
# Generate Django SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Generate JWT_SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Then update your `.env` file with the generated keys:
```bash
SECRET_KEY=your-generated-django-secret-key
JWT_SECRET_KEY=your-generated-jwt-secret-key
```

## 🔍 **Verify File Creation**

After creating the `.env` file, you should see it in your project directory:
```bash
ls -la /home/zeyadhoussainy/alx-BE-graduation-project-ECommerce/
```

You should see:
```
.env
manage.py
requirements.txt
...
```

## ✅ **What This Fixes**

- ✅ **Missing environment configuration** - Django will now find your settings
- ✅ **Database connection** - Proper MySQL credentials
- ✅ **Security settings** - Production-ready configuration
- ✅ **Static files** - Correct paths for PythonAnywhere
- ✅ **CORS settings** - Proper domain configuration

## 🚀 **Next Steps**

After creating the `.env` file:
1. **Fix the WSGI configuration** (Fix 1)
2. **Run the setup script** to install dependencies
3. **Reload your web app**

**Your Django app should now have all the environment variables it needs! 🎯**
