# PythonAnywhere Deployment Fix Instructions

## Issues Found and Fixed:

### 1. **CRITICAL: Wrong Django Settings Module**
- **Problem**: WSGI file was pointing to `'alx-BE-graduation-project-ECommerce.settings'`
- **Solution**: Should point to `'ecommerce_api.settings'` (your actual Django project name)

### 2. **Missing pkg_resources Package**
- **Problem**: `rest_framework_simplejwt` requires `pkg_resources` from `setuptools`
- **Solution**: Added `setuptools==70.0.0` to requirements.txt

## **ACTIONS YOU NEED TO TAKE ON PYTHONANYWHERE:**

### Step 1: Update WSGI Configuration File
1. Go to your PythonAnywhere **Web** tab
2. Click on your website configuration
3. Find the **WSGI configuration file** link: `/var/www/zeyadhoussainy_pythonanywhere_com_wsgi.py`
4. Replace the entire content with this:

```python
# PythonAnywhere WSGI configuration file for Django project

import os
import sys

# Add your project directory to the Python path
path = '/home/zeyadhoussainy/alx-BE-graduation-project-ECommerce'
if path not in sys.path:
    sys.path.insert(0, path)

# Set the Django settings module - CORRECTED
os.environ['DJANGO_SETTINGS_MODULE'] = 'ecommerce_api.settings'

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### Step 2: Install Missing Dependencies
1. Open a **Console** in PythonAnywhere
2. Activate your virtual environment:
   ```bash
   source /home/zeyadhoussainy/venv/bin/activate
   ```
3. Install setuptools specifically:
   ```bash
   pip install setuptools==70.0.0
   ```
4. Install all requirements from your updated file:
   ```bash
   cd /home/zeyadhoussainy/alx-BE-graduation-project-ECommerce
   pip install -r requirements.txt
   ```

### Step 3: Verify Virtual Environment Configuration
1. In your **Web** tab, make sure the **Virtualenv** field is set to:
   ```
   /home/zeyadhoussainy/venv
   ```

### Step 4: Set Working Directory
1. In your **Web** tab, make sure the **Working directory** is set to:
   ```
   /home/zeyadhoussainy/alx-BE-graduation-project-ECommerce/
   ```

### Step 5: Check Environment Variables (if any)
1. If your Django app uses environment variables (like database credentials), add them in the **Environment variables** section of your Web tab

### Step 6: Reload Your Web App
1. Click the green **"Reload"** button in your Web tab
2. Wait for the reload to complete

### Step 7: Test Your Website
1. Visit: https://zeyadhoussainy.pythonanywhere.com/
2. Check the error logs if there are still issues

## **Additional Debugging Steps (if needed):**

### Check Error Logs:
1. Go to **Web** tab
2. Click on **Error log** link
3. Look for any new error messages

### Check if Django can import properly:
1. Open a console
2. Activate virtual environment
3. Run:
   ```bash
   cd /home/zeyadhoussainy/alx-BE-graduation-project-ECommerce
   python manage.py check
   ```

### Test imports in Python console:
```python
import os
import sys
sys.path.insert(0, '/home/zeyadhoussainy/alx-BE-graduation-project-ECommerce')
os.environ['DJANGO_SETTINGS_MODULE'] = 'ecommerce_api.settings'
import django
django.setup()
```

## **Key Points:**
- The main issue was the incorrect settings module path in WSGI
- Your Django project is named `ecommerce_api`, not `alx-BE-graduation-project-ECommerce`
- The repository name and Django project name are different
- Adding setuptools will resolve the pkg_resources import error

After following these steps, your website should work correctly!
