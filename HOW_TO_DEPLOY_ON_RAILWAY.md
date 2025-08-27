# How to Deploy Django E-commerce API on Railway

This guide will walk you through deploying your Django E-commerce API project on Railway step by step.

## Prerequisites

- A Railway account (sign up at [railway.app](https://railway.app))
- Your Django project code pushed to a Git repository (GitHub, GitLab, etc.)
- Basic knowledge of Git and command line

## Step 1: Prepare Your Project

Your project is already prepared with all necessary files:
- ✅ `Procfile` - Tells Railway how to run your app
- ✅ `runtime.txt` - Specifies Python version
- ✅ `build.sh` - Build script for deployment
- ✅ `railway.json` - Railway configuration
- ✅ `requirements.txt` - Python dependencies
- ✅ Updated `settings.py` - Production-ready settings

## Step 2: Create a Railway Account

1. Go to [railway.app](https://railway.app)
2. Click "Sign Up" and create an account
3. Verify your email address

## Step 3: Connect Your Repository

1. **Login to Railway Dashboard**
   - Go to [railway.app](https://railway.app)
   - Click "Login" and sign in

2. **Create New Project**
   - Click "New Project" button
   - Select "Deploy from GitHub repo"
   - Connect your GitHub account if not already connected
   - Select your Django E-commerce repository

3. **Configure Repository**
   - Railway will automatically detect it's a Python project
   - Set the root directory to `/` (root of your project)
   - Click "Deploy Now"

## Step 4: Add Database Service

1. **Add MySQL Database**
   - In your Railway project dashboard, click "New"
   - Select "Database" → "MySQL"
   - Give it a name (e.g., "ecommerce-db")
   - Click "Add"

2. **Configure Database Variables**
   - Railway will automatically provide these environment variables:
     - `MYSQLDATABASE`
     - `MYSQLHOST`
     - `MYSQLUSERNAME`
     - `MYSQLPASSWORD`
     - `MYSQLPORT`

## Step 5: Configure Environment Variables

1. **Go to Variables Tab**
   - In your Railway project dashboard, click "Variables" tab

2. **Add Required Variables**
   ```bash
   # Django Settings
   SECRET_KEY=your-super-secret-key-here-make-it-long-and-random
   DEBUG=False
   ALLOWED_HOSTS=*.railway.app,your-app-name.railway.app
   RAILWAY_ENVIRONMENT=True
   
   # Security Settings
   CSRF_TRUSTED_ORIGINS=https://*.railway.app
   SECURE_SSL_REDIRECT=True
   SESSION_COOKIE_SECURE=True
   CSRF_COOKIE_SECURE=True
   
   # JWT Settings
   JWT_SECRET_KEY=your-jwt-secret-key-here
   JWT_ACCESS_TOKEN_LIFETIME=1
   JWT_REFRESH_TOKEN_LIFETIME=7
   
   # CORS Settings
   CORS_ALLOWED_ORIGINS=https://*.railway.app,http://localhost:3000
   
   # Static and Media Files
   STATIC_ROOT=/app/staticfiles
   MEDIA_ROOT=/app/media
   
   # Logging
   LOG_LEVEL=INFO
   ```

3. **Generate Secret Keys**
   - For `SECRET_KEY`, use Django's built-in generator:
     ```bash
     python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
     ```
   - For `JWT_SECRET_KEY`, generate another random string

## Step 6: Deploy Your Application

1. **Trigger Deployment**
   - Railway will automatically deploy when you push to your main branch
   - Or manually trigger by clicking "Deploy" in the dashboard

2. **Monitor Build Process**
   - Watch the build logs in real-time
   - The build script will:
     - Install dependencies
     - Collect static files
     - Run database migrations

3. **Check Deployment Status**
   - Green checkmark means successful deployment
   - Click on your service to see the URL

## Step 7: Verify Deployment

1. **Test Your API**
   - Visit your Railway URL (e.g., `https://your-app.railway.app`)
   - Test API endpoints
   - Check admin interface at `/admin/`

2. **Check Database Connection**
   - Verify data is being stored/retrieved
   - Check Railway logs for any database errors

3. **Test Static Files**
   - Ensure CSS/JS files are loading
   - Check media file uploads

## Step 8: Configure Custom Domain (Optional)

1. **Add Custom Domain**
   - In Railway dashboard, go to "Settings" → "Domains"
   - Click "Add Domain"
   - Enter your custom domain
   - Update DNS records as instructed

2. **Update Environment Variables**
   - Add your custom domain to:
     - `ALLOWED_HOSTS`
     - `CSRF_TRUSTED_ORIGINS`
     - `CORS_ALLOWED_ORIGINS`

## Step 9: Set Up Continuous Deployment

1. **Automatic Deployments**
   - Railway automatically deploys on every push to your main branch
   - No manual intervention needed

2. **Environment-Specific Deployments**
   - Create different branches for staging/production
   - Set up separate Railway projects if needed

## Troubleshooting Common Issues

### Build Failures
- Check build logs for specific error messages
- Ensure all dependencies are in `requirements.txt`
- Verify Python version compatibility

### Database Connection Issues
- Check database service is running
- Verify environment variables are correct
- Ensure database is accessible from your app

### Static Files Not Loading
- Check `STATIC_ROOT` and `STATIC_URL` settings
- Verify WhiteNoise is properly configured
- Check build logs for static file collection

### 500 Server Errors
- Check Railway logs for detailed error messages
- Verify `DEBUG=False` in production
- Check database migrations completed successfully

## Monitoring and Maintenance

1. **View Logs**
   - Access logs in Railway dashboard
   - Monitor for errors and performance issues

2. **Scale Application**
   - Adjust number of replicas in Railway dashboard
   - Monitor resource usage

3. **Database Backups**
   - Railway provides automatic backups
   - Download backups from database service dashboard

## Security Best Practices

1. **Environment Variables**
   - Never commit secrets to Git
   - Use Railway's secure variable storage
   - Rotate secrets regularly

2. **HTTPS**
   - Railway provides automatic SSL certificates
   - Ensure `SECURE_SSL_REDIRECT=True`

3. **CORS Configuration**
   - Only allow necessary origins
   - Restrict to your frontend domains

## Cost Optimization

1. **Free Tier**
   - Railway offers free tier with limitations
   - Monitor usage to avoid charges

2. **Resource Limits**
   - Set appropriate resource limits
   - Scale down during low traffic periods

## Support and Resources

- [Railway Documentation](https://docs.railway.app/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/)
- [Railway Community Discord](https://discord.gg/railway)

## Final Notes

Your Django E-commerce API is now production-ready and deployed on Railway! The platform will automatically handle:
- SSL certificates
- Load balancing
- Automatic scaling
- Database management
- Continuous deployment

Remember to:
- Monitor your application regularly
- Keep dependencies updated
- Test thoroughly before major releases
- Maintain proper backup strategies

Happy deploying! 🚀
