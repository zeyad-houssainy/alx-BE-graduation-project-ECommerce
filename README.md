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

## Tech Stack

- **Backend**: Django 5.2.4
- **API**: Django REST Framework
- **Authentication**: JWT (JSON Web Tokens)
- **Database**: MySQL (with PostgreSQL support for Railway)
- **Static Files**: WhiteNoise
- **Server**: Gunicorn
- **Deployment**: Railway-ready

## Quick Start

### Prerequisites

- Python 3.11+
- MySQL database
- Git

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd alx-BE-graduation-project-ECommerce
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp railway.env.template .env
   # Edit .env with your local database credentials
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - API Root: http://localhost:8000/
   - Admin Interface: http://localhost:8000/admin/
   - API Documentation: http://localhost:8000/docs/

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

## Deployment

This project is fully prepared for deployment on Railway. See [HOW_TO_DEPLOY_ON_RAILWAY.md](HOW_TO_DEPLOY_ON_RAILWAY.md) for complete deployment instructions.

### Railway Deployment Features

- ✅ Automatic build and deployment
- ✅ MySQL database integration
- ✅ Static file handling
- ✅ Environment variable management
- ✅ SSL/HTTPS support
- ✅ Health checks
- ✅ Auto-scaling capabilities

## Environment Variables

### Required Variables
- `SECRET_KEY`: Django secret key
- `DEBUG`: Debug mode (False for production)
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `RAILWAY_ENVIRONMENT`: Set to True for Railway deployment

### Database Variables (Auto-provided by Railway)
- `MYSQLDATABASE`: Database name
- `MYSQLHOST`: Database host
- `MYSQLUSERNAME`: Database username
- `MYSQLPASSWORD`: Database password
- `MYSQLPORT`: Database port

### Security Variables
- `CSRF_TRUSTED_ORIGINS`: CSRF trusted origins
- `SECURE_SSL_REDIRECT`: Enable SSL redirect
- `SESSION_COOKIE_SECURE`: Secure session cookies
- `CSRF_COOKIE_SECURE`: Secure CSRF cookies

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For deployment support, refer to the [Railway deployment guide](HOW_TO_DEPLOY_ON_RAILWAY.md).

For general support, please open an issue in the repository.

