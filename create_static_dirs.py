#!/usr/bin/env python3
"""
Script to create static directory and prepare for PythonAnywhere deployment
"""

import os
import sys

def create_static_directory():
    """Create static directory if it doesn't exist"""
    static_dir = '/home/zeyadhoussainy/alx-BE-graduation-project-ECommerce/static'
    
    if not os.path.exists(static_dir):
        os.makedirs(static_dir, exist_ok=True)
        print(f"✅ Created static directory: {static_dir}")
        
        # Create subdirectories
        subdirs = ['css', 'js', 'images']
        for subdir in subdirs:
            subdir_path = os.path.join(static_dir, subdir)
            os.makedirs(subdir_path, exist_ok=True)
            print(f"✅ Created subdirectory: {subdir_path}")
            
        # Create README
        readme_path = os.path.join(static_dir, 'README.md')
        with open(readme_path, 'w') as f:
            f.write("""# Static Files Directory

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
""")
        print(f"✅ Created README: {readme_path}")
    else:
        print(f"✅ Static directory already exists: {static_dir}")

if __name__ == '__main__':
    create_static_directory()
