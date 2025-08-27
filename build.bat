@echo off
REM Build script for Railway deployment (Windows version)

echo Starting build process...

REM Install dependencies
pip install -r requirements.txt

REM Collect static files
python manage.py collectstatic --noinput

REM Run database migrations
python manage.py migrate

REM Create superuser if it doesn't exist (optional)
REM python manage.py createsuperuser --noinput

echo Build process completed!
