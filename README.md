# 🛒 Django E-commerce API

A comprehensive Django REST API for an e-commerce platform with user authentication, product management, categories, and reviews.

## 📸 Home Page Screenshot

![Home Page](images/homepage.jpg)
*Modern and responsive home page with gradient background, action buttons for mock data generation, and comprehensive feature overview*

---

## ✨ Features

- **🔐 User Authentication**: JWT-based authentication system
- **📦 Product Management**: CRUD operations for products with image support
- **🏷️ Category Management**: Hierarchical category system
- **👤 User Profiles**: Extended user profiles with additional information
- **⭐ Product Reviews**: Rating and review system for products
- **🌐 RESTful API**: Full REST API with filtering, searching, and pagination
- **⚙️ Admin Interface**: Django admin for content management
- **🌍 CORS Support**: Cross-origin resource sharing enabled
- **📁 Static File Handling**: Optimized static file serving for production
- **🎲 Mock Data Generation**: One-click sample data creation for testing
- **👥 Mock Users Generation**: Comprehensive user account creation for testing

---

## 🛠️ Tech Stack

- **Backend**: Django 5.2.4
- **API**: Django REST Framework
- **Authentication**: JWT (JSON Web Tokens)
- **Database**: MySQL 8.0+
- **Static Files**: Django built-in static file handling
- **Server**: Development server

---

## 🚀 Quick Start (Local Development)

### Prerequisites

- **Python 3.11+** - [Download Python](https://www.python.org/downloads/)
- **MySQL 8.0+** - [Download MySQL](https://dev.mysql.com/downloads/mysql/)
- **Git** - [Download Git](https://git-scm.com/downloads)

### Step 1: Clone & Setup

```bash
# Clone the repository
git clone https://github.com/zeyad-houssainy/alx-BE-graduation-project-ECommerce
cd alx-BE-graduation-project-ECommerce

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Database Setup

#### Option A: Automatic Setup (Recommended)

```bash
# On Windows
setup_local.bat

# On macOS/Linux
python setup_local.bat
```

#### Option B: Manual Setup

1. **Start MySQL Service**
   ```bash
   # Windows (as Administrator)
   net start mysql
   
   # macOS
   brew services start mysql
   
   # Linux
   sudo systemctl start mysql
   ```

2. **Create Database**
   ```bash
   python create_database.py
   python setup_mysql.py
   ```

### Step 3: Environment Configuration

1. **Copy environment template**
   ```bash
   cp env_template.txt .env
   ```

2. **Edit `.env` file with your database credentials**
   ```env
   # Database Configuration
   DB_NAME=ecommerce_db
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=your_password_here
   DB_PORT=3306
   
   # Django Settings
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ```

3. **⚠️ Important**: Change the default password in `ecommerce_api/settings.py` from `'zeyad203'` to your own secure password

### Step 4: Run Django

```bash
# Apply database migrations
python manage.py makemigrations
python manage.py migrate

# Collect static files
python manage.py collectstatic

# Start development server
python manage.py runserver
```

### Step 5: Access Your Application

- **Main Site**: http://localhost:8000/
- **Admin Panel**: http://localhost:8000/admin/
- **API Root**: http://localhost:8000/api/

### Step 6: Login Credentials

**Default Superuser Account:**
- **Username**: `admin`
- **Password**: `admin`
- **Email**: `admin@admin.com`

---

## 📚 Detailed Installation Guide

### Environment Variables

Create a `.env` file with these settings:

```env
# Django Core Settings
SECRET_KEY=your-super-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DB_NAME=ecommerce_db
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your-chosen-password
DB_PORT=3306

# JWT Settings
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ACCESS_TOKEN_LIFETIME=1
JWT_REFRESH_TOKEN_LIFETIME=7

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Static and Media Files
STATIC_ROOT=./staticfiles
MEDIA_ROOT=./media
```

### Generate Secret Keys

```bash
# Generate Django SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Generate JWT_SECRET_KEY (can be same as Django SECRET_KEY)
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## 🌐 API Endpoints

The project includes comprehensive REST API endpoints:

- **Authentication**: `/api/auth/` - JWT token management
- **Users**: `/api/users/` - User management and profiles
- **Categories**: `/api/categories/` - Category management
- **Products**: `/api/products/` - Product management with filtering
- **Reviews**: `/api/reviews/` - Product reviews and ratings

All endpoints support:
- Filtering and searching
- Pagination
- Authentication requirements
- Comprehensive documentation

---

## 🚀 Deployment

### PythonAnywhere Deployment

This project is configured for easy deployment on PythonAnywhere:

**📖 Full Deployment Guide**: [DEPLOY_PYTHONANYWHERE.md](DEPLOY_PYTHONANYWHERE.md)

**⚡ Quick Deployment**:
1. Clone repository on PythonAnywhere
2. Create MySQL database
3. Configure environment variables
4. Install dependencies and run migrations
5. Configure web app and WSGI file
6. Reload and test

---

## 🛠️ Development Commands

```bash
# Django Management
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
python manage.py runserver

# Testing
python test_mysql.py

# Virtual Environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
```

---

## 🔧 Troubleshooting

**Common Issues:**

- **MySQL Connection Error**: Ensure MySQL service is running
- **Database Access Denied**: Check credentials in `.env` file
- **Module Not Found**: Run `pip install -r requirements.txt`
- **Port Already in Use**: Use different port or kill existing process

---

## 📸 Project Screenshots

### Home Page
![Home Page](images/homepage.jpg)
*Modern and responsive home page with gradient background, action buttons for mock data generation, and comprehensive feature overview*

### Home Page Overview
![Home Page Overview](images/home%20page%20overview.jpg)
*Complete home page view showcasing navigation, hero section, feature cards, and action buttons for the e-commerce platform*

### CRUD Dashboard
![CRUD Dashboard](images/CRUD%20dashboard.jpg)
*Main dashboard interface with real-time statistics cards, quick actions, and comprehensive overview of products, categories, and users*

### API Endpoints
![API Endpoints](images/API%20endpoints.jpg)
*Structured overview of API endpoints and technology stack with clear categorization and technical details*

### API Interface
![API Interface](images/API.jpg)
*Interactive API dashboard showing endpoint categories, authentication requirements, and quick access to documentation*

### Category Management
![Category Management](images/Category%20management.jpg)
*Advanced category management interface with search, filtering, and full CRUD operations for organizing products*

### Admin Panel
![Admin Panel](images/admin%20panel.jpg)
*Django admin interface with dark theme for managing user accounts, authentication, categories, and products*

### Admin Products Management
![Admin Products Management](images/admin%20page%20products.jpg)
*Comprehensive product management in Django admin with advanced filtering, search capabilities, and bulk operations*

### API Documentation
![API Documentation](images/documentation.jpg)
*Detailed API documentation with authentication examples, request/response formats, and comprehensive endpoint guides*

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

---

## 📄 License

This project is part of the ALX Backend Engineering graduation project.

---

## 🔗 Quick Links

- [Full Deployment Guide](DEPLOY_PYTHONANYWHERE.md)
- [PythonAnywhere Checklist](PYTHONANYWHERE_CHECKLIST.md)
- [Requirements](requirements.txt)
- [Environment Template](env_template.txt)



