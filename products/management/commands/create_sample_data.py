from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
import random
from decimal import Decimal
from categories.models import Category
from products.models import Product
from accounts.models import UserProfile


class Command(BaseCommand):
    help = 'Create sample data for testing the e-commerce API'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating sample data...'))
        
        categories = self.create_categories()
        users = self.create_users()
        products = self.create_products(categories, users)
        
        self.display_summary(categories, users, products)

    def create_categories(self):
        """Create sample categories"""
        categories_data = [
            {'name': 'Electronics', 'description': 'Electronic devices and gadgets'},
            {'name': 'Clothing', 'description': 'Fashion and apparel'},
            {'name': 'Books', 'description': 'Books and literature'},
            {'name': 'Sports', 'description': 'Sports equipment and gear'},
            {'name': 'Home & Garden', 'description': 'Home improvement and gardening'},
            {'name': 'Beauty', 'description': 'Beauty and personal care products'},
        ]

        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'description': cat_data['description'],
                    'slug': slugify(cat_data['name']),
                    'is_active': True
                }
            )
            categories.append(category)
            if created:
                self.stdout.write(f'Created category: {category.name}')
        return categories

    def create_users(self):
        """Create sample users"""
        users_data = [
            {'username': 'john_doe', 'email': 'john@example.com', 'first_name': 'John', 'last_name': 'Doe'},
            {'username': 'jane_smith', 'email': 'jane@example.com', 'first_name': 'Jane', 'last_name': 'Smith'},
            {'username': 'bob_wilson', 'email': 'bob@example.com', 'first_name': 'Bob', 'last_name': 'Wilson'},
            {'username': 'alice_brown', 'email': 'alice@example.com', 'first_name': 'Alice', 'last_name': 'Brown'},
        ]

        users = []
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'is_active': True
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                # Create user profile only if it doesn't exist
                UserProfile.objects.get_or_create(user=user)
                self.stdout.write(f'Created user: {user.username}')
            else:
                # Get or create profile for existing user
                UserProfile.objects.get_or_create(user=user)
                self.stdout.write(f'User already exists: {user.username}')
            users.append(user)

        # Add admin user if exists
        try:
            admin_user = User.objects.get(username='admin')
            users.append(admin_user)
        except User.DoesNotExist:
            pass
            
        return users

    def create_products(self, categories, users):
        """Create sample products"""
        products_data = [
            {'name': 'iPhone 15 Pro', 'description': 'Latest Apple smartphone with advanced features', 'price': '999.99', 'stock': 50},
            {'name': 'Samsung Galaxy S24', 'description': 'Premium Android smartphone', 'price': '899.99', 'stock': 30},
            {'name': 'MacBook Air M3', 'description': 'Lightweight laptop with M3 chip', 'price': '1299.99', 'stock': 20},
            {'name': 'Nike Air Max 270', 'description': 'Comfortable running shoes', 'price': '150.00', 'stock': 100},
            {'name': 'Adidas Ultraboost 22', 'description': 'High-performance running shoes', 'price': '180.00', 'stock': 75},
            {'name': 'The Great Gatsby', 'description': 'Classic American novel by F. Scott Fitzgerald', 'price': '12.99', 'stock': 200},
            {'name': 'Python Programming Guide', 'description': 'Comprehensive guide to Python programming', 'price': '45.99', 'stock': 50},
            {'name': 'Yoga Mat Premium', 'description': 'High-quality yoga mat for professionals', 'price': '79.99', 'stock': 40},
            {'name': 'Gaming Chair Pro', 'description': 'Ergonomic gaming chair with RGB lighting', 'price': '299.99', 'stock': 15},
            {'name': 'Moisturizing Face Cream', 'description': 'Anti-aging face cream with natural ingredients', 'price': '34.99', 'stock': 80},
        ]

        products = []
        for i, prod_data in enumerate(products_data):
            category = categories[i % len(categories)]
            creator = random.choice(users)
            
            product, created = Product.objects.get_or_create(
                name=prod_data['name'],
                defaults={
                    'description': prod_data['description'],
                    'price': Decimal(prod_data['price']),
                    'category': category,
                    'stock_quantity': prod_data['stock'],
                    'is_active': True,
                    'created_by': creator,
                    'slug': slugify(prod_data['name'])
                }
            )
            products.append(product)
            if created:
                self.stdout.write(f'Created product: {product.name}')

        return products

    def display_summary(self, categories, users, products):
        """Display summary of created data"""
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Sample data created successfully!\n'
                f'📊 Summary:\n'
                f'   - Categories: {len(categories)}\n'
                f'   - Users: {len(users)}\n'
                f'   - Products: {len(products)}\n\n'
                f'🔗 You can now:\n'
                f'   - Visit: http://127.0.0.1:8000/api/\n'
                f'   - Browse products: http://127.0.0.1:8000/api/products/\n'
                f'   - View categories: http://127.0.0.1:8000/api/categories/\n'
                f'   - Login to admin: http://127.0.0.1:8000/admin/ (admin/admin123)'
            )
        )
