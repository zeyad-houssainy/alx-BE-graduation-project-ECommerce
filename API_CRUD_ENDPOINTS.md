# E-commerce API - Complete CRUD Endpoints Documentation

This document provides a comprehensive list of all CRUD (Create, Read, Update, Delete) endpoints available in the E-commerce API.

## Base URL
```
http://127.0.0.1:8000/api/
```

## Authentication
Most endpoints require authentication using JWT tokens. Include the token in the Authorization header:
```
Authorization: Bearer <your_access_token>
```

## 1. Authentication Endpoints

### User Registration
- **POST** `/api/auth/register/`
- **Description**: Register a new user account
- **Request Body**:
```json
{
    "username": "newuser",
    "email": "user@example.com",
    "password": "securepassword123",
    "first_name": "John",
    "last_name": "Doe"
}
```

### User Login
- **POST** `/api/auth/login/`
- **Description**: Login and get JWT tokens
- **Request Body**:
```json
{
    "username": "newuser",
    "password": "securepassword123"
}
```

### JWT Token Management
- **POST** `/api/token/` - Get access and refresh tokens
- **POST** `/api/token/refresh/` - Refresh access token
- **POST** `/api/token/verify/` - Verify token validity

## 2. Products Endpoints

### Basic CRUD Operations
- **GET** `/api/products/` - List all products
- **POST** `/api/products/` - Create a new product
- **GET** `/api/products/{slug}/` - Retrieve a specific product
- **PUT** `/api/products/{slug}/` - Update a product (full update)
- **PATCH** `/api/products/{slug}/` - Update a product (partial update)
- **DELETE** `/api/products/{slug}/` - Delete a product (soft delete)

### Additional Product Actions
- **GET** `/api/products/search/?q=query` - Search products
- **GET** `/api/products/featured/` - Get featured products
- **GET** `/api/products/out-of-stock/` - Get out of stock products
- **GET** `/api/products/low-stock/` - Get products with low stock
- **POST** `/api/products/{slug}/update_stock/` - Update product stock
- **POST** `/api/products/{slug}/toggle_active/` - Toggle product active status

### Bulk Operations
- **POST** `/api/products/bulk-update/` - Bulk update products
- **DELETE** `/api/products/bulk-delete/` - Bulk delete products

### Product Request Examples

#### Create Product
```json
POST /api/products/
{
    "name": "New Product",
    "description": "Product description",
    "price": "99.99",
    "category": 1,
    "stock_quantity": 50,
    "is_active": true
}
```

#### Update Product Stock
```json
POST /api/products/new-product/update_stock/
{
    "stock_quantity": 25
}
```

#### Bulk Update Products
```json
POST /api/products/bulk-update/
{
    "product_ids": [1, 2, 3],
    "update_data": {
        "is_active": false,
        "price": "89.99"
    }
}
```

## 3. Categories Endpoints

### Basic CRUD Operations
- **GET** `/api/categories/` - List all categories
- **POST** `/api/categories/` - Create a new category
- **GET** `/api/categories/{slug}/` - Retrieve a specific category
- **PUT** `/api/categories/{slug}/` - Update a category (full update)
- **PATCH** `/api/categories/{slug}/` - Update a category (partial update)
- **DELETE** `/api/categories/{slug}/` - Delete a category (soft delete)

### Additional Category Actions
- **GET** `/api/categories/{slug}/products/` - Get products in a category
- **GET** `/api/categories/featured/` - Get featured categories
- **GET** `/api/categories/popular/` - Get popular categories
- **GET** `/api/categories/search/?q=query` - Search categories
- **GET** `/api/categories/{slug}/stats/` - Get category statistics
- **POST** `/api/categories/{slug}/toggle_active/` - Toggle category active status

### Bulk Operations
- **POST** `/api/categories/bulk-update/` - Bulk update categories
- **DELETE** `/api/categories/bulk-delete/` - Bulk delete categories

### Category Request Examples

#### Create Category
```json
POST /api/categories/
{
    "name": "New Category",
    "description": "Category description",
    "is_active": true
}
```

#### Get Category Statistics
```json
GET /api/categories/electronics/stats/
```

#### Bulk Update Categories
```json
POST /api/categories/bulk-update/
{
    "category_ids": [1, 2, 3],
    "update_data": {
        "is_active": false
    }
}
```

## 4. Users Endpoints

### Basic CRUD Operations (Admin Only)
- **GET** `/api/users/` - List all users (admin only)
- **POST** `/api/users/` - Create a new user
- **GET** `/api/users/{id}/` - Retrieve a specific user
- **PUT** `/api/users/{id}/` - Update a user (full update)
- **PATCH** `/api/users/{id}/` - Update a user (partial update)
- **DELETE** `/api/users/{id}/` - Delete a user

### User Profile Management
- **GET** `/api/users/profile/` - Get current user's profile
- **PUT** `/api/users/update_profile/` - Update current user's profile
- **PATCH** `/api/users/update_profile/` - Update current user's profile (partial)

### Additional User Actions
- **GET** `/api/users/search/?q=query` - Search users (admin only)
- **POST** `/api/users/{id}/toggle_active/` - Toggle user active status (admin only)

### Bulk Operations (Admin Only)
- **POST** `/api/users/bulk-update/` - Bulk update users
- **DELETE** `/api/users/bulk-delete/` - Bulk delete users

### User Request Examples

#### Update User Profile
```json
PUT /api/users/update_profile/
{
    "phone_number": "+1234567890",
    "address": "123 Main St, City, Country",
    "date_of_birth": "1990-01-01"
}
```

#### Bulk Update Users
```json
POST /api/users/bulk-update/
{
    "user_ids": [1, 2, 3],
    "update_data": {
        "is_active": false,
        "first_name": "Updated"
    }
}
```

## 5. User Profiles Endpoints

### Basic CRUD Operations
- **GET** `/api/profiles/` - List user profiles (admin only)
- **POST** `/api/profiles/` - Create a new profile
- **GET** `/api/profiles/{id}/` - Retrieve a specific profile
- **PUT** `/api/profiles/{id}/` - Update a profile (full update)
- **PATCH** `/api/profiles/{id}/` - Update a profile (partial update)
- **DELETE** `/api/profiles/{id}/` - Delete a profile

### Profile Request Examples

#### Create Profile
```json
POST /api/profiles/
{
    "user": 1,
    "phone_number": "+1234567890",
    "address": "123 Main St, City, Country",
    "date_of_birth": "1990-01-01"
}
```

## 6. Query Parameters

### Pagination
- `?page=1` - Page number
- `?page_size=20` - Items per page

### Filtering
- `?category=electronics` - Filter by category
- `?is_active=true` - Filter by active status
- `?price_min=10&price_max=100` - Filter by price range

### Searching
- `?search=keyword` - Search in name and description
- `?q=query` - Advanced search (for specific endpoints)

### Ordering
- `?ordering=name` - Order by name (ascending)
- `?ordering=-price` - Order by price (descending)
- `?ordering=created_at` - Order by creation date

## 7. Response Formats

### Success Response
```json
{
    "id": 1,
    "name": "Product Name",
    "description": "Product description",
    "price": "99.99",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
}
```

### Error Response
```json
{
    "error": "Error message",
    "detail": "Detailed error information"
}
```

### Paginated Response
```json
{
    "count": 100,
    "next": "http://127.0.0.1:8000/api/products/?page=2",
    "previous": null,
    "results": [...]
}
```

## 8. Status Codes

- **200** - OK (Success)
- **201** - Created (Resource created successfully)
- **400** - Bad Request (Invalid data)
- **401** - Unauthorized (Authentication required)
- **403** - Forbidden (Permission denied)
- **404** - Not Found (Resource not found)
- **500** - Internal Server Error

## 9. Testing the API

### Using curl
```bash
# Get all products
curl -H "Authorization: Bearer <token>" http://127.0.0.1:8000/api/products/

# Create a product
curl -X POST -H "Authorization: Bearer <token>" \
     -H "Content-Type: application/json" \
     -d '{"name":"Test Product","price":"99.99","category":1}' \
     http://127.0.0.1:8000/api/products/

# Update a product
curl -X PUT -H "Authorization: Bearer <token>" \
     -H "Content-Type: application/json" \
     -d '{"name":"Updated Product","price":"89.99","category":1}' \
     http://127.0.0.1:8000/api/products/test-product/

# Delete a product
curl -X DELETE -H "Authorization: Bearer <token>" \
     http://127.0.0.1:8000/api/products/test-product/
```

### Using the Django REST Framework Browsable API
Visit `http://127.0.0.1:8000/api/` in your browser to access the interactive API documentation.

## 10. Admin Interface

Access the Django admin interface at `http://127.0.0.1:8000/admin/` to manage:
- Users and User Profiles
- Categories
- Products
- Authentication and Authorization

Login with your superuser credentials (admin/admin).
