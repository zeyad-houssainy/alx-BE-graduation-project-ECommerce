# Static Files Directory

This directory contains static files for the Django project:

- `css/` - Custom CSS stylesheets
- `js/` - Custom JavaScript files  
- `images/` - Static images (logos, icons, etc.)

## Usage

Place your custom static files here. Django will collect them during deployment using:

```bash
python manage.py collectstatic
```

For development, make sure `DEBUG = True` and Django will serve these files automatically.

For production (like PythonAnywhere), run `collectstatic` to copy files to `STATIC_ROOT` directory.
