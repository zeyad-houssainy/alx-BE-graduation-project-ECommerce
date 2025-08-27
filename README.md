# 🛒 E-Commerce API Project

A modern, scalable e-commerce API built with Django REST Framework, featuring a comprehensive web interface for data management and a robust REST API for developers.

## 🚀 Quick Setup

### Option 1: Clone (Recommended)
```bash
git clone https://github.com/yourusername/alx-BE-graduation-project-ECommerce.git
cd alx-BE-graduation-project-ECommerce
```

### Option 2: Fork
1. Click the "Fork" button on GitHub
2. Clone your forked repository:
```bash
git clone https://github.com/YOUR_USERNAME/alx-BE-graduation-project-ECommerce.git
cd alx-BE-graduation-project-ECommerce
```

## ⚡ Quick Start

### 1. Environment Setup
```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (Mac/Linux)
source .venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Database Configuration
Create `.env` file in project root:
```bash
# Django Settings
SECRET_KEY=django-insecure-your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# MySQL Database
DB_NAME=ecommerce_db
DB_USER=root
DB_PASSWORD=your-mysql-password  # Make sure to change this into your own password
DB_HOST=localhost
DB_PORT=3306

# JWT Settings
JWT_SECRET_KEY=your-jwt-secret
JWT_ACCESS_TOKEN_LIFETIME=1
JWT_REFRESH_TOKEN_LIFERY=7
```

### 4. Database Setup
```bash
# Create MySQL database
mysql -u root -p -e "CREATE DATABASE ecommerce_db;"

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 5. Run Development Server
```bash
python manage.py runserver
```

Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) 🎉

## ✨ Main Features

### 🔐 **Authentication System**
- JWT-based authentication
- User registration and login
- Role-based access control (User, Staff, Admin)
- Secure password management

### 📦 **Product Management**
- Full CRUD operations for products
- Category organization
- Image upload and management
- Stock quantity tracking
- Search and filtering capabilities

### 👥 **User Management**
- User profiles and preferences
- Admin user management
- Secure user authentication
- Profile customization

### 🏷️ **Category System**
- Hierarchical category organization
- SEO-friendly slugs
- Product categorization
- Category management interface

### 🌐 **Web Interface**
- **CRUD Dashboard**: Full web-based data management
- **Admin Panel**: Django admin interface
- **Responsive Design**: Mobile-friendly interface
- **Real-time Search**: Instant data filtering

### 🔌 **RESTful API**
- Complete REST API endpoints
- JWT authentication
- Comprehensive documentation
- Developer-friendly responses

### 🗄️ **Database & Performance**
- MySQL database integration
- Optimized database queries
- Database migrations
- Performance monitoring

### 🛡️ **Security Features**
- CSRF protection
- Input validation
- Secure file uploads
- Role-based permissions

## 🎯 **Key Endpoints**

- **Authentication**: `/api/auth/register/`, `/api/auth/login/`
- **Users**: `/api/users/`
- **Products**: `/api/products/`
- **Categories**: `/api/categories/`
- **API Root**: `/api/`
- **Documentation**: `/docs/`

## 🛠️ **Tech Stack**

- **Backend**: Django 5.2.4 + Django REST Framework
- **Database**: MySQL 8.0
- **Authentication**: JWT (JSON Web Tokens)
- **Frontend**: Bootstrap 5 + FontAwesome
- **Python**: 3.11+

## 📱 **Access Points**

- **Home**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **API**: [http://127.0.0.1:8000/api/](http://127.0.0.1:8000/api/)
- **CRUD Dashboard**: [http://127.0.0.1:8000/crud/](http://127.0.0.1:8000/crud/)
- **Admin**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
- **Documentation**: [http://127.0.0.1:8000/docs/](http://127.0.0.1:8000/docs/)

## 🚀 **Ready to Use**

This project provides everything you need for a production-ready e-commerce API:
- ✅ Complete user authentication
- ✅ Full product management
- ✅ Web-based admin interface
- ✅ RESTful API endpoints
- ✅ Comprehensive documentation
- ✅ Security best practices

---

**Built with ❤️ using Django REST Framework**
