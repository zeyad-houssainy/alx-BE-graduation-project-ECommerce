from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
import random
from categories.models import Category
from products.models import Product
from accounts.models import UserProfile

class Command(BaseCommand):
    help = 'Generate basic sample data for the e-commerce project (MySQL compatible)'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('Starting basic data generation for MySQL...')
        )
        
        # Create categories
        categories = self.create_categories()
        
        # Create users
        users = self.create_users()
        
        # Create products
        products = self.create_products(categories, users)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created:\n'
                f'- {len(categories)} categories\n'
                f'- {len(users)} users\n'
                f'- {len(products)} products'
            )
        )

    def create_categories(self):
        """Create basic product categories"""
        categories = []
        category_data = [
            ('Electronics', 'Electronic devices and accessories'),
            ('Clothing', 'Apparel and fashion items'),
            ('Home & Garden', 'Home improvement and garden supplies'),
            ('Sports', 'Sports equipment and athletic gear'),
            ('Books', 'Books and educational materials'),
        ]
        
        for name, description in category_data:
            category, created = Category.objects.get_or_create(
                name=name,
                defaults={
                    'slug': slugify(name),
                    'description': description,
                    'is_active': True
                }
            )
            categories.append(category)
            if created:
                self.stdout.write(f'Created category: {name}')
        
        return categories

    def create_users(self):
        """Create sample users"""
        users = []
        user_data = [
            ('admin', 'admin@example.com', 'admin'),
            ('user1', 'user1@example.com', 'password123'),
            ('user2', 'user2@example.com', 'password123'),
        ]
        
        for username, email, password in user_data:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'first_name': username.capitalize(),
                    'last_name': 'User',
                    'is_active': True
                }
            )
            if created:
                user.set_password(password)
                user.save()
                # Create profile
                UserProfile.objects.create(user=user)
                self.stdout.write(f'Created user: {username}')
            users.append(user)
        
        return users

    def create_products(self, categories, users):
        """Create sample products"""
        products = []
        product_data = [
            ('Smartphone', 'Latest smartphone with advanced features', 599.99, 'Electronics'),
            ('Laptop', 'High-performance laptop for work and gaming', 999.99, 'Electronics'),
            ('T-Shirt', 'Comfortable cotton t-shirt', 19.99, 'Clothing'),
            ('Jeans', 'Classic blue jeans', 49.99, 'Clothing'),
            ('Garden Tool Set', 'Essential tools for gardening', 79.99, 'Home & Garden'),
            ('Basketball', 'Official size basketball', 29.99, 'Sports'),
            ('Python Programming Book', 'Learn Python programming', 39.99, 'Books'),
        ]
        
        for name, description, price, category_name in product_data:
            category = next((c for c in categories if c.name == category_name), categories[0])
            creator = random.choice(users)
            
            product, created = Product.objects.get_or_create(
                name=name,
                defaults={
                    'slug': slugify(name),
                    'description': description,
                    'price': price,
                    'category': category,
                    'stock_quantity': random.randint(10, 100),
                    'is_active': True,
                    'created_by': creator
                }
            )
            if created:
                self.stdout.write(f'Created product: {name}')
            products.append(product)
        
        return products
