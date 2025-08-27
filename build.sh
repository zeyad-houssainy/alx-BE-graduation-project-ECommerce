#!/bin/bash

# Build script for Railway deployment

echo "Starting build process..."

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run database migrations
python manage.py migrate

# Create superuser if it doesn't exist (optional)
# python manage.py createsuperuser --noinput

echo "Build process completed!"
