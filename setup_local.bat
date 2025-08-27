@echo off
echo === Django E-commerce API - Complete Local Setup ===
echo.

echo Step 1: Installing dependencies...
pip install -r requirements.txt

echo.
echo Step 2: Checking and fixing MySQL service...
python fix_mysql_service.py

echo.
echo Step 3: Setting up MySQL database and user...
python create_database.py

echo.
echo Step 4: Running Django setup...
python setup_mysql.py

echo.
echo Step 5: Creating superuser...
python manage.py createsuperuser

echo.
echo === Setup Complete! ===
echo.
echo To start the development server, run:
echo python manage.py runserver
echo.
echo To test your setup, run:
echo python test_mysql.py
echo.
pause
