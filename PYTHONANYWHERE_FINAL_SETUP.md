# PythonAnywhere Complete Setup Instructions

## Quick Setup (Recommended)

1. **Open a Bash Console** on PythonAnywhere
2. **Navigate to your project directory:**
   ```bash
   cd /home/zeyadhoussainy/alx-BE-graduation-project-ECommerce
   ```

3. **Run the complete setup script:**
   ```bash
   python pythonanywhere_complete_setup.py
   ```

This script will automatically:
- ✅ Detect PythonAnywhere environment
- ✅ Create static directory structure
- ✅ Run database migrations
- ✅ Create admin user (admin/admin)
- ✅ Collect static files
- ✅ Display final instructions

## Manual Setup (Alternative)

If you prefer to run commands individually:

### 1. Create Static Directory
```bash
python create_static_dirs.py
```

### 2. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py create_mock_users
```

### 3. Static Files
```bash
python manage.py collectstatic --noinput
```

## Final Check

After setup, test these URLs:

- **Main Website:** https://zeyadhoussainy.pythonanywhere.com
- **Admin Panel:** https://zeyadhoussainy.pythonanywhere.com/admin/
- **API Root:** https://zeyadhoussainy.pythonanywhere.com/api/

### Admin Credentials
- **Username:** `admin`
- **Password:** `admin`

## Troubleshooting

### Database Issues
If you get connection errors, the auto-detection should work. The settings.py now automatically detects PythonAnywhere and uses MySQL.

### Static Files Issues
If CSS/JS don't load, run:
```bash
python manage.py collectstatic --noinput
```

### Permission Issues
If you get permission errors:
```bash
chmod +x pythonanywhere_complete_setup.py
python pythonanywhere_complete_setup.py
```

## Environment Detection

The project now automatically detects if it's running on PythonAnywhere by checking the hostname. This means:

- **On PythonAnywhere:** Uses MySQL database (`zeyadhoussainy$default`)
- **Locally:** Uses SQLite database (`db.sqlite3`)

No manual configuration needed! 🎉

## Support

If you encounter any issues:

1. Check the PythonAnywhere error logs
2. Verify your database credentials in the PythonAnywhere MySQL section
3. Ensure your web app is configured to use the correct Python version
4. Make sure the WSGI file path is correct: `/home/zeyadhoussainy/alx-BE-graduation-project-ECommerce/ecommerce_api/wsgi.py`
