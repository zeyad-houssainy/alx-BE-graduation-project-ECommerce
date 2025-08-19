# 🛒 E-Commerce Product API

A Django-based e-commerce API with basic CRUD operations, user authentication, and product management. This project is currently in development with core functionality implemented.

## 📚 **Quick Links for Mentors & Reviewers**

- **🚀 Quick Setup**: Run `python setup_for_mentor.py` for automated setup
- **👨‍🏫 Mentor Guide**: See [MENTOR_GUIDE.md](MENTOR_GUIDE.md) for detailed review instructions
- **📖 Full Documentation**: This README contains comprehensive setup and usage instructions

## 🌟 Features

### Core Features
- **Product Management**: Basic CRUD operations for products with categories
- **User Management**: User registration, authentication, and basic profile management
- **Category Management**: Product categorization and organization
- **Authentication**: JWT-based authentication with refresh tokens
- **API Design**: RESTful API with proper HTTP status codes
- **Database**: MySQL database with Django ORM
- **Image Handling**: Basic product image upload

### Current Status
- **Basic CRUD operations** ✅
- **User authentication** ✅
- **Product management** ✅
- **Category management** ✅
- **Basic API endpoints** ✅

## 🏗️ Architecture

### Technology Stack
- **Backend Framework**: Django 5.2.4 - High-level Python web framework
- **API Framework**: Django REST Framework 3.15.2 - Powerful toolkit for building Web APIs
- **Authentication**: Django REST Framework SimpleJWT 5.3.0 - JSON Web Token authentication
- **Database**: MySQL 8.0+ - Robust relational database for production use
- **Image Processing**: Pillow 10.4.0 - Python Imaging Library for image handling
- **Filtering & Search**: Django Filter 24.3 - Basic filtering capabilities
- **CORS Handling**: django-cors-headers 4.5.0 - Cross-Origin Resource Sharing
- **Environment Management**: python-decouple 3.8 - Environment variables handling
- **Static Files**: WhiteNoise 6.8.1 - Efficient static file serving

### 📦 Dependencies (requirements.txt)
```txt
Django==5.2.4
djangorestframework==3.15.2
djangorestframework-simplejwt==5.3.0
django-filter==24.3
django-cors-headers==4.5.0
Pillow==10.4.0
python-decouple==3.8
mysqlclient==2.2.7
whitenoise==6.8.1
gunicorn==23.0.0
```

### Project Structure
```
alx-BE-graduation-project-ECommerce/
├── accounts/                 # User management app
│   ├── models.py            # UserProfile model
│   ├── views.py             # User views and authentication
│   ├── serializers.py       # User data serialization
│   └── urls.py              # User-related URL patterns
├── categories/               # Product categories app
│   ├── models.py            # Category model
│   ├── views.py             # Category management views
│   ├── serializers.py       # Category data serialization
│   └── urls.py              # Category URL patterns
├── products/                 # Product management app
│   ├── models.py            # Product model
│   ├── views.py             # Product management views
│   ├── serializers.py       # Product data serialization
│   ├── filters.py           # Basic product filtering
│   └── urls.py              # Product URL patterns
├── ecommerce_api/            # Main project configuration
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL routing
│   └── management/          # Basic management commands
├── templates/                # HTML templates
├── static/                   # Static files
├── media/                    # User-uploaded files
├── .env                      # Environment variables (create from env_example.txt)
└── requirements.txt          # Python dependencies
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+ (recommended)
- MySQL 8.0+ server installed and running
- pip (Python package manager)
- Git (for version control)

### 1. Clone the Repository
```bash
git clone https://github.com/zeyad-houssainy/alx-BE-graduation-project-ECommerce.git
cd alx-BE-graduation-project-ECommerce
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. MySQL Database Setup
```sql
-- Connect to MySQL as root
mysql -u root -p

-- Create database
CREATE DATABASE ecommerce_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create user (optional, for production)
CREATE USER 'ecommerce_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON ecommerce_db.* TO 'ecommerce_user'@'localhost';
FLUSH PRIVILEGES;

-- Exit MySQL
EXIT;
```

### 5. Environment Configuration
```bash
# Copy environment file
cp env_example.txt .env

# Edit .env file with your MySQL credentials
# Update DB_PASSWORD and other settings as needed
```

### 6. Database Setup
```bash
# Run migrations to create MySQL database tables
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Superuser
```bash
python manage.py createsuperuser
# Follow the prompts to create admin user
```

### 8. Run Development Server
```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

### 9. Access Admin Panel
Visit `http://127.0.0.1:8000/admin/` and login with your superuser credentials.

### 10. Create Sample Data (Optional)
```bash
# Generate large dataset for monitoring (500 products + 200 users)
python manage.py generate_large_dataset --clear

# Or basic sample data
python manage.py create_sample_data
```

## 👨‍🏫 **For Mentors & Reviewers**

### **🎯 Project Overview for Review**
This is an **ALX Backend Engineering Graduation Project** demonstrating:
- **Django REST Framework** mastery
- **MySQL database** integration
- **JWT authentication** implementation
- **Complete CRUD operations** with proper validation
- **Admin interface** customization
- **API documentation** and testing

### **📊 Current Progress: 60% Complete**

#### **✅ What's Implemented:**
- **User Authentication System**
  - JWT token-based authentication
  - User registration/login with validation
  - User profiles with extended information
  
- **Product Management**
  - Full CRUD operations for products
  - Category-based organization
  - Stock management with alerts
  - Image upload handling
  
- **Category Management**
  - Hierarchical product categorization
  - CRUD operations with validation
  
- **Admin Interface**
  - Custom Django admin with dashboard
  - Enhanced data visualization
  - Bulk operations for efficiency
  
- **API Design**
  - RESTful endpoints following best practices
  - Proper HTTP status codes
  - Comprehensive error handling
  - Search and filtering capabilities

#### **🔄 What's In Progress:**
- Advanced filtering and search optimization
- Performance improvements for large datasets
- Enhanced security features

#### **📋 Planned Features (Future Development):**
- Product reviews and ratings system
- Wishlist functionality
- Order management system
- Shopping cart implementation
- Payment gateway integration
- Email notification system
- Advanced analytics dashboard

### **🚀 Quick Setup for Mentors**

#### **Prerequisites Check:**
```bash
# Check Python version (3.11+ required)
python --version

# Check if MySQL is running
mysql --version

# Check if pip is available
pip --version
```

#### **One-Command Setup (if you have Docker):**
```bash
# Clone and setup in one go
git clone https://github.com/yourusername/alx-BE-graduation-project-ECommerce.git
cd alx-BE-graduation-project-ECommerce

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup database (make sure MySQL is running)
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Generate sample data
python manage.py generate_large_dataset --clear

# Run server
python manage.py runserver
```

#### **Manual Database Setup:**
```sql
-- Connect to MySQL as root
mysql -u root -p

-- Create database
CREATE DATABASE storefront2 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Exit MySQL
EXIT;
```

### **🧪 Testing the Project**

#### **1. Check Admin Panel**
- Visit: `http://127.0.0.1:8000/admin/`
- Login with your superuser credentials
- Explore the enhanced admin interface with dashboard

#### **2. Test API Endpoints**
```bash
# Test public endpoints (no auth required)
curl http://127.0.0.1:8000/api/products/
curl http://127.0.0.1:8000/api/categories/

# Test authentication
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "mentor", "email": "mentor@example.com", "password": "mentor123", "password_confirm": "mentor123", "first_name": "Mentor", "last_name": "User"}'
```

#### **3. Verify Data Generation**
- Check that you have 500+ products and 200+ users
- Verify categories are properly populated
- Test search and filtering functionality

### **📈 What to Look For During Review**

#### **Code Quality:**
- **Models**: Well-structured Django models with proper relationships
- **Views**: Clean ViewSet implementations with proper permissions
- **Serializers**: Comprehensive data validation and transformation
- **URLs**: RESTful endpoint design following conventions

#### **Features:**
- **Authentication**: JWT implementation with refresh tokens
- **CRUD Operations**: Complete create, read, update, delete functionality
- **Admin Interface**: Custom admin with enhanced user experience
- **API Design**: Proper HTTP methods, status codes, and error handling

#### **Database:**
- **MySQL Integration**: Proper database configuration and migrations
- **Data Relationships**: Foreign keys and related queries working correctly
- **Performance**: Efficient queries with select_related and prefetch_related

#### **Security:**
- **Input Validation**: Proper data sanitization and validation
- **Authentication**: Secure token-based authentication
- **Permissions**: Role-based access control implementation

### **🔍 Key Files to Review**

#### **Core Models:**
- `products/models.py` - Product and category models
- `accounts/models.py` - User profile model
- `ecommerce_api/models.py` - Any project-wide models

#### **API Views:**
- `products/views.py` - Product CRUD operations
- `categories/views.py` - Category management
- `accounts/views.py` - User authentication and management

#### **Admin Customization:**
- `ecommerce_api/admin.py` - Custom admin site with dashboard
- `templates/admin/dashboard.html` - Admin dashboard template

#### **Configuration:**
- `ecommerce_api/settings.py` - Database and app configuration
- `requirements.txt` - Dependencies and versions

### **💡 Questions to Ask During Review**

1. **Architecture**: How well does the project follow Django best practices?
2. **API Design**: Are the endpoints RESTful and well-documented?
3. **Database**: How efficient are the database queries and relationships?
4. **Security**: Are authentication and permissions properly implemented?
5. **User Experience**: How intuitive is the admin interface?
6. **Code Quality**: Is the code readable, maintainable, and well-structured?
7. **Testing**: Are there sufficient tests for the implemented features?
8. **Documentation**: Is the README comprehensive and helpful?

### **🎯 Evaluation Criteria**

#### **Excellent (90-100%):**
- All CRUD operations working perfectly
- Clean, well-documented code
- Proper error handling and validation
- Enhanced admin interface
- Comprehensive API documentation

#### **Good (80-89%):**
- Most features working correctly
- Good code structure
- Basic admin functionality
- API endpoints functional

#### **Satisfactory (70-79%):**
- Core functionality working
- Basic CRUD operations
- Simple admin interface
- API responding to requests

#### **Needs Improvement (<70%):**
- Major functionality missing
- Code structure issues
- Admin interface problems
- API errors or crashes

---

## 📡 API Endpoints

### Products
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/products/` | List all products | No |
| POST | `/api/products/` | Create new product | Yes |
| GET | `/api/products/{slug}/` | Get product details | No |
| PUT | `/api/products/{slug}/` | Update product | Yes |
| DELETE | `/api/products/{slug}/` | Delete product | Yes |

### Categories
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/categories/` | List all categories | No |
| POST | `/api/categories/` | Create new category | Yes |
| GET | `/api/categories/{slug}/` | Get category details | No |
| PUT | `/api/categories/{slug}/` | Update category | Yes |
| DELETE | `/api/categories/{slug}/` | Delete category | Yes |

### Users
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/users/` | List users | Yes |
| POST | `/api/users/` | Create user | Yes |
| GET | `/api/users/{id}/` | Get user details | Yes |
| PUT | `/api/users/{id}/` | Update user | Yes |
| DELETE | `/api/users/{id}/` | Delete user | Yes |

### User Profiles
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/profiles/` | List user profiles | Yes |
| GET | `/api/profiles/{id}/` | Get profile details | Yes |
| PUT | `/api/profiles/{id}/` | Update profile | Yes |

### Authentication
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/register/` | User registration | No |
| POST | `/api/auth/login/` | User login | No |

## 🛠️ CRUD Commands & Examples

### 🔐 **Step 1: Authentication (Get JWT Token)**

Before performing CRUD operations, you need to authenticate and get a JWT token:

#### **User Registration**
```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "password_confirm": "testpass123",
    "first_name": "Test",
    "last_name": "User"
  }'
```

#### **User Login (Get JWT Token)**
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Save the access token for subsequent requests:**
```bash
export TOKEN="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

### 📁 **Step 2: Category Management (CRUD)**

#### **Create Category**
```bash
curl -X POST http://127.0.0.1:8000/api/categories/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "name": "Electronics",
    "description": "Electronic devices and gadgets"
  }'
```

#### **List All Categories**
```bash
curl -X GET http://127.0.0.1:8000/api/categories/ \
  -H "Content-Type: application/json"
```

#### **Get Category Details**
```bash
curl -X GET http://127.0.0.1:8000/api/categories/electronics/ \
  -H "Content-Type: application/json"
```

#### **Update Category**
```bash
curl -X PUT http://127.0.0.1:8000/api/categories/electronics/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "name": "Electronics & Gadgets",
    "description": "Updated description for electronics category"
  }'
```

#### **Delete Category**
```bash
curl -X DELETE http://127.0.0.1:8000/api/categories/electronics/ \
  -H "Authorization: Bearer $TOKEN"
```

### 📦 **Step 3: Product Management (CRUD)**

#### **Create Product**
```bash
curl -X POST http://127.0.0.1:8000/api/products/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "name": "iPhone 15 Pro",
    "description": "Latest iPhone with advanced features",
    "price": "999.99",
    "category": 1,
    "stock_quantity": 50
  }'
```

#### **List All Products**
```bash
curl -X GET http://127.0.0.1:8000/api/products/ \
  -H "Content-Type: application/json"
```

#### **Get Product Details**
```bash
curl -X GET http://127.0.0.1:8000/api/products/iphone-15-pro/ \
  -H "Content-Type: application/json"
```

#### **Update Product**
```bash
curl -X PUT http://127.0.0.1:8000/api/products/iphone-15-pro/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "name": "iPhone 15 Pro Max",
    "description": "Updated description",
    "price": "1099.99",
    "stock_quantity": 45
  }'
```

#### **Delete Product**
```bash
curl -X DELETE http://127.0.0.1:8000/api/products/iphone-15-pro/ \
  -H "Authorization: Bearer $TOKEN"
```

### 👥 **Step 4: User Management (CRUD)**

#### **Create User (Admin Only)**
```bash
curl -X POST http://127.0.0.1:8000/api/users/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "username": "newuser",
    "email": "newuser@example.com",
    "password": "newpass123",
    "first_name": "New",
    "last_name": "User"
  }'
```

#### **List All Users (Admin Only)**
```bash
curl -X GET http://127.0.0.1:8000/api/users/ \
  -H "Authorization: Bearer $TOKEN"
```

#### **Get User Details**
```bash
curl -X GET http://127.0.0.1:8000/api/users/2/ \
  -H "Authorization: Bearer $TOKEN"
```

#### **Update User**
```bash
curl -X PUT http://127.0.0.1:8000/api/users/2/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "first_name": "Updated",
    "last_name": "Name",
    "email": "updated@example.com"
  }'
```

#### **Delete User**
```bash
curl -X DELETE http://127.0.0.1:8000/api/users/2/ \
  -H "Authorization: Bearer $TOKEN"
```

### 🔍 **Step 5: Advanced Product Operations**

#### **Search Products**
```bash
curl -X GET "http://127.0.0.1:8000/api/products/?search=iphone" \
  -H "Content-Type: application/json"
```

#### **Filter by Category**
```bash
curl -X GET "http://127.0.0.1:8000/api/products/?category=1" \
  -H "Content-Type: application/json"
```

#### **Filter by Price Range**
```bash
curl -X GET "http://127.0.0.1:8000/api/products/?price__gte=100&price__lte=1000" \
  -H "Content-Type: application/json"
```

#### **Get Featured Products**
```bash
curl -X GET http://127.0.0.1:8000/api/products/featured/ \
  -H "Content-Type: application/json"
```

#### **Get Low Stock Products**
```bash
curl -X GET http://127.0.0.1:8000/api/products/low_stock/ \
  -H "Content-Type: application/json"
```

### 📊 **Step 6: Bulk Operations**

#### **Bulk Update Products**
```bash
curl -X POST http://127.0.0.1:8000/api/products/bulk_update/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "product_ids": [1, 2, 3],
    "update_data": {
      "is_active": true,
      "stock_quantity": 100
    }
  }'
```

#### **Bulk Delete Products**
```bash
curl -X POST http://127.0.0.1:8000/api/products/bulk_delete/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "product_ids": [1, 2, 3]
  }'
```

### 🖼️ **Step 7: File Upload Examples**

#### **Upload Product Image**
```bash
curl -X POST http://127.0.0.1:8000/api/products/ \
  -H "Authorization: Bearer $TOKEN" \
  -F "name=Product with Image" \
  -F "description=Product description" \
  -F "price=99.99" \
  -F "category=1" \
  -F "stock_quantity=25" \
  -F "image=@/path/to/your/image.jpg"
```

#### **Upload Profile Picture**
```bash
curl -X PUT http://127.0.0.1:8000/api/profiles/1/ \
  -H "Authorization: Bearer $TOKEN" \
  -F "profile_picture=@/path/to/your/profile.jpg"
```

### 🔄 **Step 8: Token Management**

#### **Refresh Token**
```bash
curl -X POST http://127.0.0.1:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "your_refresh_token_here"
  }'
```

#### **Verify Token**
```bash
curl -X POST http://127.0.0.1:8000/api/token/verify/ \
  -H "Content-Type: application/json" \
  -d '{
    "token": "your_access_token_here"
  }'
```

### 📱 **Step 9: Using with Different Tools**

#### **Using Postman**
1. Set base URL: `http://127.0.0.1:8000`
2. Add header: `Authorization: Bearer <your_token>`
3. Use the endpoints above with Postman's interface

#### **Using Python Requests**
```python
import requests

# Base URL
base_url = "http://127.0.0.1:8000/api"

# Headers
headers = {
    "Authorization": "Bearer your_token_here",
    "Content-Type": "application/json"
}

# Create product
product_data = {
    "name": "Test Product",
    "description": "Test Description",
    "price": "99.99",
    "category": 1,
    "stock_quantity": 10
}

response = requests.post(f"{base_url}/products/", json=product_data, headers=headers)
print(response.json())
```

#### **Using JavaScript/Fetch**
```javascript
const baseUrl = 'http://127.0.0.1:8000/api';
const token = 'your_token_here';

// Create product
fetch(`${baseUrl}/products/`, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({
        name: 'Test Product',
        description: 'Test Description',
        price: '99.99',
        category: 1,
        stock_quantity: 10
    })
})
.then(response => response.json())
.then(data => console.log(data));
```

### ⚠️ **Important Notes**

1. **Authentication Required**: Most CRUD operations require a valid JWT token
2. **Admin Access**: User management operations require admin privileges
3. **Soft Delete**: Products and categories use soft delete (is_active = False)
4. **Image Uploads**: Use `multipart/form-data` for file uploads
5. **Validation**: All data is validated before processing
6. **Rate Limiting**: Consider implementing rate limiting for production

### 🧪 **Testing Your CRUD Operations**

1. **Start the server**: `python manage.py runserver`
2. **Generate sample data**: `python manage.py generate_large_dataset`
3. **Test authentication**: Use the login endpoint to get a token
4. **Test CRUD operations**: Use the examples above with your token
5. **Check admin panel**: Visit `/admin/` to see your data

## 🔍 Product Filtering & Search

### Available Filters
- **Search**: `?search=keyword` - Search in product name, description, and category
- **Category**: `?category=id` - Filter by category ID
- **Price Range**: `?price__gte=100&price__lte=500` - Filter by price range

### Example Filter Requests
```bash
# Search for smartphones
curl "http://127.0.0.1:8000/api/products/?search=smartphone"

# Filter by category
curl "http://127.0.0.1:8000/api/products/?category=1"

# Filter by price range
curl "http://127.0.0.1:8000/api/products/?price__gte=100&price__lte=500"
```

## 📊 Data Models

### Product Model
```python
class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    stock_quantity = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/')
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### Category Model
```python
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='categories/', blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### UserProfile Model
```python
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
```

## 🔐 Authentication

### JWT Token Endpoints
- **Login**: `POST /api/auth/login/`
- **Register**: `POST /api/auth/register/`
- **Token Refresh**: `POST /api/token/refresh/`
- **Token Verify**: `POST /api/token/verify/`

### Authentication Headers
```http
Authorization: Bearer <access_token>
```

### Example Login Request
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin"}'
```

## 🚀 Deployment

### Production Deployment
1. Set `DEBUG = False` in settings
2. Configure production MySQL database
3. Set `ALLOWED_HOSTS` for your domain
4. Configure static files collection
5. Set up environment variables

### Environment Variables
Create a `.env` file from `env_example.txt`:
```env
SECRET_KEY=your-secret-key-here
DEBUG=False
DB_NAME=your_production_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=3306
ALLOWED_HOSTS=your-domain.com
```

### Static Files Collection
```bash
python manage.py collectstatic
```

### Gunicorn Deployment
```bash
gunicorn ecommerce_api.wsgi:application --bind 0.0.0.0:8000
```

## 🔒 Security Features

### Authentication & Authorization
- JWT token-based authentication
- Role-based access control
- Secure password validation
- CSRF protection

### Data Validation
- Input sanitization
- SQL injection prevention (MySQL prepared statements)
- XSS protection
- File upload validation

## 🛠️ Custom Management Commands

### Generate Sample Data
```bash
# Large dataset for monitoring (500 products + 200 users)
python manage.py generate_large_dataset --clear

# Basic sample data
python manage.py create_sample_data
```

## 📝 API Documentation

### Response Format
All API responses follow a consistent format:
```json
{
    "count": 100,
    "next": "http://api.example.org/accounts/?page=4",
    "previous": "http://api.example.org/accounts/?page=2",
    "results": [...]
}
```

### Error Handling
```json
{
    "error": "Error message",
    "detail": "Detailed error information"
}
```

### Status Codes
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `500` - Internal Server Error

## 🎯 Project Status

**Current Status: 60% Complete**

This project implements the core e-commerce functionality:
- ✅ Basic product management
- ✅ User authentication system
- ✅ Category management
- ✅ RESTful API design
- ✅ Basic filtering and search
- ✅ MySQL database integration

**Planned Features (Future Development):**
- [ ] Product reviews and ratings
- [ ] Wishlist functionality
- [ ] Advanced filtering options
- [ ] Order management
- [ ] Shopping cart
- [ ] Payment integration
- [ ] Email notifications
- [ ] Advanced analytics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the documentation

---

**Built with ❤️ using Django and MySQL**

*Note: This project is currently in active development. Some features may be incomplete or subject to change.*
