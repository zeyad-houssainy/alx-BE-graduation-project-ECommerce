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
- **Database**: MySQL (with PostgreSQL support for Railway)
- **Static Files**: WhiteNoise
- **Server**: Gunicorn


## Mock Data Feature

The project includes a powerful mock data generation system that allows you to quickly populate your database with realistic sample data for testing and development purposes.

### **What You Get:**
- 🎯 **Ready-to-use data** for immediate API testing
- 🔧 **Debugging scenarios** with realistic e-commerce data
- 📊 **30 Sample products** across 8 categories
- 👥 **5 Test users** with complete profiles
- 🏷️ **8 Product categories** for organized testing
- 💰 **Realistic pricing** and stock quantities
- 📱 **Complete product details** with descriptions and images support

### **How to Use:**
1. **Web Interface**: Click "Create Mock Data" button on the home page
2. **Command Line**: Run `python manage.py create_mock_data`
3. **Instant Results**: Get 30 products, 8 categories, and 5 users in seconds

### **Perfect For:**
- 🧪 **API Testing**: Test all endpoints with real data
- 🔍 **Development**: Debug with realistic scenarios
- 📚 **Learning**: Understand the system with sample data
- 🚀 **Quick Setup**: Get started immediately after installation

### **Categories & Products Created:**

**🏷️ 8 Product Categories:**
- **Electronics**: Latest gadgets and devices
- **Clothing**: Fashion and apparel items
- **Books**: Various genres and subjects
- **Home & Garden**: Household and garden items
- **Sports**: Athletic equipment and gear
- **Toys & Games**: Entertainment for all ages
- **Automotive**: Car accessories and parts
- **Health & Beauty**: Wellness and beauty products

**📦 30 Sample Products Include:**
- **Electronics**: Smartphone X ($699.99), Laptop Pro ($1299.99), Wireless Headphones ($199.99), Smart Watch ($299.99)
- **Clothing**: Classic T-Shirt ($24.99), Denim Jeans ($79.99), Winter Jacket ($149.99), Running Shoes ($89.99)
- **Books**: The Great Adventure ($19.99), Programming Guide ($49.99), Cookbook Deluxe ($34.99), History of Science ($29.99)
- **Home & Garden**: Garden Tool Set ($89.99), Kitchen Mixer ($199.99), LED Desk Lamp ($59.99), Plant Pot Set ($39.99)
- **Sports**: Basketball ($29.99), Yoga Mat ($44.99), Tennis Racket ($129.99), Fitness Tracker ($89.99)
- **Toys & Games**: Board Game Set ($39.99), Remote Control Car ($79.99), Puzzle Collection ($24.99)
- **Automotive**: Car Phone Mount ($19.99), LED Light Strip ($34.99)
- **Health & Beauty**: Skincare Set ($89.99), Hair Dryer Pro ($129.99)

**👥 5 Test Users Created:**
- **Admin User**: `admin/admin123` (superuser with full access)
- **Regular Users**: `john_doe/password123`, `jane_smith/password123`, `bob_wilson/password123`, `alice_brown/password123`
- **Complete Profiles**: Phone numbers, addresses, cities, states, zip codes

### **After Creating Mock Data:**
- 🧪 **Test API Endpoints**: All endpoints now have real data to work with
- 📊 **Explore CRUD Dashboard**: View and manage products, categories, and users
- 🔐 **Test Authentication**: Login with any of the created user accounts
- 📱 **Admin Interface**: Access `/admin/` with admin/admin123 credentials
- 🚀 **Immediate Development**: Start building and testing features right away

## Mock Users Feature

The project also includes a dedicated mock users generation system that creates comprehensive user accounts for testing authentication, permissions, and user management features.

### **What You Get:**
- 👥 **Multiple User Types**: Superusers, staff users, and regular users
- 🔐 **Permission Testing**: Different access levels for role-based testing
- 📱 **Complete Profiles**: Realistic contact information and addresses
- 🧪 **Authentication Testing**: Ready-to-use login credentials
- 👔 **Staff Management**: Test different permission levels

### **User Types Created:**
- **👑 Superusers**: Full system access (admin/admin123)
- **👔 Staff Users**: Limited admin access (manager_kate/password123, support_alex/password123)
- **👤 Regular Users**: Standard user accounts (john_doe/password123, mike_johnson/password123, etc.)

### **Profile Information:**
- **Phone Numbers**: Random US phone numbers
- **Addresses**: Realistic street addresses across major US cities
- **Geographic Data**: Various states, cities, and zip codes
- **Contact Details**: Complete user profile information

### **Perfect For:**
- 🔐 **Authentication Testing**: Test login/logout functionality
- 👥 **User Management**: Test CRUD operations on users
- 🚫 **Permission Testing**: Test role-based access control
- 📱 **Profile Testing**: Test extended user profile features
- 🧪 **Security Testing**: Test different user permission levels

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.11+** - [Download Python](https://www.python.org/downloads/)
- **MySQL 8.0+** - [Download MySQL](https://dev.mysql.com/downloads/mysql/)
- **Git** - [Download Git](https://git-scm.com/downloads)
- **pip** (usually comes with Python)

## Installation Guide

### Step 1: Clone the Repository

```bash
git clone <your-repo-url>
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
cp railway.env.template .env
```

#### Configure Database Settings

Edit your `.env` file with the following database information:

```env
# Django Core Settings
SECRET_KEY=your-super-secret-key-here-make-it-long-and-random
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
RAILWAY_ENVIRONMENT=False

# Local MySQL Database Configuration
DB_NAME=ecommerce_db
DB_HOST=localhost
DB_USER=ecommerce_user
DB_PASSWORD=your-chosen-password
DB_PORT=3306

# Alternative: Use root user (not recommended for production)
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
- Use different passwords for development and production

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
- Email address (e.g., `admin@example.com`)
- Password (make it strong and secure)
- Password confirmation

**Example:**
```bash
Username: admin
Email address: admin@example.com
Password: ********
Password (again): ********
Superuser created successfully.
```

**⚠️ Important:** Remember your admin credentials - you'll need them to access `/admin/` and manage your application.

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

For debugging and testing purposes, you can easily populate your database with sample data. This is perfect for:
- 🧪 Testing API endpoints
- 🔍 Debugging functionality
- 📚 Learning how the system works
- 🚀 Quick development setup

#### **Option A: Web Interface (Recommended)**
1. Start your server: `python manage.py runserver`
2. Go to the home page: http://localhost:8000/
3. Choose your option:
   - **"Create Mock Data"** button (yellow) - Creates products, categories, and basic users
   - **"Create Mock Users"** button (blue) - Creates comprehensive user accounts with profiles
4. Wait for the confirmation message
5. Your database will be populated with sample data!

#### **Option B: Command Line**
```bash
# Create products, categories, and basic users
python manage.py create_mock_data

# Create comprehensive user accounts with profiles
python manage.py create_mock_users
```

#### **What Gets Created:**

**Mock Data (Products & Categories):**
- ✅ **Admin User**: `admin/admin123` (superuser with full access)
- ✅ **Basic Users**: `john_doe/password123`, `jane_smith/password123`, `bob_wilson/password123`, `alice_brown/password123`
- ✅ **8 Categories**: Electronics, Clothing, Books, Home & Garden, Sports, Toys & Games, Automotive, Health & Beauty
- ✅ **30 Products**: Realistic products across all categories with prices, descriptions, and stock levels
- ✅ **User Profiles**: Complete contact information for basic users

**Mock Users (Comprehensive User Management):**
- ✅ **Admin User**: `admin/admin123` (superuser with full access)
- ✅ **Staff Users**: `manager_kate/password123`, `support_alex/password123` (for testing permissions)
- ✅ **Regular Users**: 10+ users with realistic names and profiles
- ✅ **User Profiles**: Complete contact information with random addresses, phones, cities
- ✅ **Permission Levels**: Different user types for testing role-based access control

#### **Sample Products Include:**
- **Electronics**: Smartphone X ($699.99), Laptop Pro ($1299.99), Wireless Headphones ($199.99)
- **Clothing**: Classic T-Shirt ($24.99), Denim Jeans ($79.99), Winter Jacket ($149.99)
- **Books**: The Great Adventure ($19.99), Programming Guide ($49.99), Cookbook Deluxe ($34.99)
- **Sports**: Basketball ($29.99), Yoga Mat ($44.99), Tennis Racket ($129.99)
- **And many more...**

#### **After Creating Mock Data:**
- Test the API endpoints with real data
- Explore the CRUD dashboard with populated information
- Use the admin interface to manage the sample data
- Practice with realistic e-commerce scenarios

### Step 11: Run Development Server

```bash
python manage.py runserver
```

## Access Your Application

- **API Root**: http://localhost:8000/
- **Admin Interface**: http://localhost:8000/admin/
- **API Documentation**: http://localhost:8000/docs/

## Troubleshooting

### Common Issues

#### 1. MySQL Connection Error
```
Error: (2003, "Can't connect to MySQL server on 'localhost'")
```
**Solution:**
- Ensure MySQL service is running
- Check if MySQL is installed correctly
- Verify port 3306 is not blocked

#### 2. Database Access Denied
```
Error: (1045, "Access denied for user 'ecommerce_user'@'localhost'")
```
**Solution:**
- Check username and password in `.env` file
- Ensure user has proper privileges
- Try connecting as root first

#### 3. Module Not Found Errors
```
ModuleNotFoundError: No module named 'mysqlclient'
```
**Solution:**
- Install MySQL client: `pip install mysqlclient`
- On Windows, you might need: `pip install pymysql`
- Ensure all requirements are installed: `pip install -r requirements.txt`

#### 4. Port Already in Use
```
Error: That port is already in use
```
**Solution:**
- Kill the process using the port: `netstat -ano | findstr :8000`
- Use a different port: `python manage.py runserver 8001`

### Getting Help

1. **Check the logs**: Look for error messages in the terminal
2. **Verify database**: Run `python test_mysql.py`
3. **Check environment**: Ensure `.env` file is properly configured
4. **Review prerequisites**: Make sure all required software is installed

## API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/refresh/` - Refresh JWT token
- `POST /api/auth/logout/` - User logout

### Users
- `GET /api/users/profile/` - Get user profile
- `PUT /api/users/profile/` - Update user profile

### Categories
- `GET /api/categories/` - List all categories
- `POST /api/categories/` - Create new category
- `GET /api/categories/{id}/` - Get category details
- `PUT /api/categories/{id}/` - Update category
- `DELETE /api/categories/{id}/` - Delete category

### Products
- `GET /api/products/` - List all products
- `POST /api/products/` - Create new product
- `GET /api/products/{id}/` - Get product details
- `PUT /api/products/{id}/` - Update product
- `DELETE /api/products/{id}/` - Delete product
- `GET /api/products/search/` - Search products

### Reviews
- `GET /api/products/{id}/reviews/` - Get product reviews
- `POST /api/products/{id}/reviews/` - Create product review
- `PUT /api/products/{id}/reviews/{review_id}/` - Update review
- `DELETE /api/products/{id}/reviews/{review_id}/` - Delete review

## Database Schema

### Users
- User authentication and profiles
- Extended profile information (phone, address, etc.)

### Categories
- Hierarchical category system
- Name, description, and parent relationships

### Products
- Product information (name, description, price, etc.)
- Image support
- Category relationships
- Stock management

### Reviews
- Product ratings and reviews
- User association
- Timestamp tracking

## Environment Variables Reference

### Required Variables
- `SECRET_KEY`: Django secret key (generate using the command above)
- `DEBUG`: Debug mode (True for development, False for production)
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `RAILWAY_ENVIRONMENT`: Set to False for local development

### Database Variables
- `DB_NAME`: Database name (default: ecommerce_db)
- `DB_HOST`: Database host (default: localhost)
- `DB_USER`: Database username (default: ecommerce_user)
- `DB_PASSWORD`: Database password (set this to your chosen password)
- `DB_PORT`: Database port (default: 3306)

### JWT Variables
- `JWT_SECRET_KEY`: JWT signing key (can be same as SECRET_KEY)
- `JWT_ACCESS_TOKEN_LIFETIME`: Access token lifetime in hours
- `JWT_REFRESH_TOKEN_LIFETIME`: Refresh token lifetime in days

### CORS Variables
- `CORS_ALLOWED_ORIGINS`: Comma-separated list of allowed origins

## Deployment

This project can be deployed on various platforms. Here are some recommended deployment options:

### Deployment Options

- **Heroku**: Easy deployment with PostgreSQL database
- **DigitalOcean App Platform**: Simple containerized deployment
- **AWS Elastic Beanstalk**: Scalable cloud deployment
- **Google Cloud Run**: Serverless container deployment
- **Vercel**: Frontend-focused deployment (may have limitations with Django)

### Deployment Preparation

Before deploying, ensure you have:
- ✅ Production-ready database (PostgreSQL recommended)
- ✅ Environment variables configured
- ✅ Static files collected
- ✅ Debug mode disabled
- ✅ Secure secret keys
- ✅ CORS properly configured for your domain

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For general support, please open an issue in the repository.

For deployment assistance, refer to the platform-specific documentation of your chosen deployment platform.

## Quick Commands Reference

```bash
# Setup
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt

# Database
python create_database.py
python setup_mysql.py

# Django
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
python manage.py runserver

# Mock Data (Optional) - Creates sample data for testing
python manage.py create_mock_data
python manage.py create_mock_users

# Mock Users (Optional) - Creates comprehensive user accounts
python manage.py create_mock_users

# Testing
python test_mysql.py
```

