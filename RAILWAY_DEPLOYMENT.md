# 🚀 Railway Deployment Guide for MySQL

This guide will help you deploy your E-Commerce API project on Railway using MySQL.

## 📋 **Prerequisites**

- GitHub repository with your project
- Railway account (free tier available)
- MySQL database (Railway provides this)

## 🚀 **Step 1: Connect to Railway**

1. Go to [railway.app](https://railway.app)
2. Sign in with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your repository: `alx-BE-graduation-project-ECommerce`

## 🗄️ **Step 2: Add MySQL Database**

1. In your Railway project dashboard, click **"New"**
2. Select **"Database"** → **"MySQL"**
3. Railway will automatically create a MySQL database
4. Note down the provided environment variables

## ⚙️ **Step 3: Configure Environment Variables**

In your Railway project dashboard, go to **"Variables"** and add:

### **Required Variables:**
```bash
# Django Settings
SECRET_KEY=your-very-long-random-secret-key-here
DEBUG=False
ALLOWED_HOSTS=*
RAILWAY_ENVIRONMENT=True

# JWT Settings
JWT_SECRET_KEY=your-jwt-secret-key-here
JWT_ACCESS_TOKEN_LIFETIME=1
JWT_REFRESH_TOKEN_LIFERY=7

# CORS Settings
CORS_ALLOWED_ORIGINS=https://*.railway.app,http://localhost:3000
```

### **MySQL Variables (Auto-provided by Railway):**
Railway automatically provides these when you add a MySQL database:
- `MYSQLDATABASE`
- `MYSQLHOST`
- `MYSQLUSERNAME`
- `MYSQLPASSWORD`
- `MYSQLPORT`

## 🔧 **Step 4: Deploy**

1. Railway will automatically detect your Django project
2. It will use the `railway.json` configuration
3. The build process will:
   - Install PyMySQL instead of mysqlclient
   - Run migrations automatically
   - Start with Gunicorn

## 📱 **Step 5: Access Your Deployed App**

After successful deployment, Railway will provide:
- **Live URL**: `https://your-app-name.railway.app`
- **API Root**: `https://your-app-name.railway.app/api/`
- **Admin Panel**: `https://your-app-name.railway.app/admin/`
- **CRUD Dashboard**: `https://your-app-name.railway.app/crud/`

## 🛠️ **Troubleshooting**

### **Build Errors:**
- ✅ **Fixed**: `mysqlclient` compilation issues by using `PyMySQL`
- ✅ **Fixed**: MySQL dependency issues by using Railway's MySQL service

### **Database Connection Issues:**
- Ensure all MySQL environment variables are set
- Check that `RAILWAY_ENVIRONMENT=True` is set
- Verify MySQL database is running in Railway

### **Static Files Issues:**
- Railway automatically serves static files
- `whitenoise` is configured for production

## 🔒 **Security Notes**

- `DEBUG=False` in production
- `SECRET_KEY` should be long and random
- `ALLOWED_HOSTS=*` allows Railway's domain
- CSRF protection is enabled for Railway domains

## 📊 **Monitoring**

Railway provides:
- **Logs**: View application logs in real-time
- **Metrics**: CPU, memory, and network usage
- **Deployments**: Automatic deployments on git push
- **Health Checks**: Automatic health monitoring

## 🚀 **Next Steps**

After deployment:
1. Create a superuser: `python manage.py createsuperuser`
2. Test all API endpoints
3. Verify database migrations
4. Check static files are served correctly

---

**Your E-Commerce API is now ready for production on Railway! 🎉**
