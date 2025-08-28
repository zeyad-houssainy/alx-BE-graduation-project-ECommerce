# Django E-commerce API

A comprehensive Django REST API for an e-commerce platform with user authentication, product management, categories, and reviews.

## Features

- **User Authentication**: JWT-based authentication system
- **Product Management**: CRUD operations for products with image support
- **Category Management**: Hierarchical category system
- **User Profiles**: Extended user profiles with additional information
- **Product Reviews**: Rating and review system for products
- **RESTful API**: Full REST API with filtering, searching, and pagination
- **Admin Interface**: Django admin for content management
- **CORS Support**: Cross-origin resource sharing enabled
- **Static File Handling**: Optimized static file serving with WhiteNoise
- **Mock Data Generation**: One-click sample data creation for testing and debugging
- **Mock Users Generation**: Comprehensive user account creation for authentication and permission testing

## Tech Stack

- **Backend**: Django 5.2.4
- **API**: Django REST Framework
- **Authentication**: JWT (JSON Web Tokens)
- **Database**: MySQL
- **Static Files**: WhiteNoise
- **Server**: Development server

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.11+** - [Download Python](https://www.python.org/downloads/)
- **MySQL 8.0+** - [Download MySQL](https://dev.mysql.com/downloads/mysql/)
- **Git** - [Download Git](https://git-scm.com/downloads)
- **pip** (usually comes with Python)

## Installation Guide

### Step 1: Clone the Repository

```bash
git clone https://github.com/zeyad-houssainy/alx-BE-graduation-project-ECommerce
cd alx-BE-graduation-project-ECommerce
```

### Step 2: Create Virtual Environment

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Database Setup

#### Option A: Automatic Setup (Recommended for Windows)

Run the automatic setup script:
```bash
# On Windows
setup_local.bat

# On macOS/Linux
python setup_local.bat
```

This script will:
- Install dependencies
- Check and fix MySQL service
- Create the database and user
- Set up Django configuration
- Create a superuser

#### Option B: Manual Database Setup

1. **Start MySQL Service**
   ```bash
   # On Windows (as Administrator)
   net start mysql
   
   # On macOS
   brew services start mysql
   
   # On Linux
   sudo systemctl start mysql
   ```

2. **Create Database and User**
   ```bash
   python create_database.py
   ```
   
   This script will:
   - Create `ecommerce_db` database
   - Create `ecommerce_user` with proper privileges
   - Test database connectivity

3. **Run Django Setup**
   ```bash
   python setup_mysql.py
   ```

### Step 5: Environment Configuration

#### Create Environment File

Copy the template and configure your environment:

```bash
cp env.example .env
```

#### Configure Database Settings

Edit your `.env` file with the following database information:

```env
# Django Core Settings
SECRET_KEY=your-super-secret-key-here-make-it-long-and-random
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Local MySQL Database Configuration
DB_NAME=ecommerce_db
DB_HOST=localhost
DB_USER=ecommerce_user
DB_PASSWORD=your-chosen-password
DB_PORT=3306

# Alternative: Use root user (not recommended for security)
# DB_NAME=ecommerce_db
# DB_HOST=localhost
# DB_USER=root
# DB_PASSWORD=your-root-password
# DB_PORT=3306

# JWT Settings
JWT_SECRET_KEY=your-jwt-secret-key-here
JWT_ACCESS_TOKEN_LIFETIME=1
JWT_REFRESH_TOKEN_LIFETIME=7

# CORS Settings for Local Development
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://localhost:8080,http://127.0.0.1:8080

# Static and Media Files
STATIC_ROOT=./staticfiles
MEDIA_ROOT=./media
```

#### Generate Secret Keys

Generate secure secret keys for Django and JWT:

```bash
# Generate Django SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Generate JWT_SECRET_KEY (can be same as Django SECRET_KEY)
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**⚠️ Important Security Notes:**
- Never commit your `.env` file to version control
- Use strong, unique passwords for database users
- Keep your secret keys secure and private
- Use different passwords for development and testing

### Step 6: Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 7: Create Superuser

Create an admin account to access the Django admin interface:

```bash
python manage.py createsuperuser
```

**Follow the prompts to enter:**
- Username (e.g., `admin`)
- Email address (e.g., `admin@admin.com`)
- Password (make it strong and secure)
- Password confirmation


### Step 8: Collect Static Files

```bash
python manage.py collectstatic
```

### Step 9: Test Your Setup

```bash
python test_mysql.py
```

This will verify that your database connection is working properly.

### Step 10: Create Sample Data (Optional)

After starting your server, use the "Create Mock Data" and "Create Mock Users" buttons on the home page to populate your database with sample data for testing.

### Step 11: Run Development Server

```bash
python manage.py runserver
```

## Access Your Application

- **API Root**: http://localhost:8000/
- **Admin Interface**: http://localhost:8000/admin/
- **API Documentation**: http://localhost:8000/docs/

## Troubleshooting

Common issues and solutions:
- **MySQL Connection**: Ensure MySQL service is running
- **Database Access**: Check credentials in `.env` file
- **Module Errors**: Install requirements with `pip install -r requirements.txt`
- **Port Issues**: Use different port or kill existing process

For detailed help, check the error messages in your terminal.

## API Endpoints

The project includes comprehensive REST API endpoints for authentication, users, categories, products, and reviews. All endpoints are documented in the code and accessible through the web interface.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request



## Quick Commands Reference

```bash
# Setup
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt

# Django
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
python manage.py runserver
```



