from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from categories.models import Category
from products.models import Product
from accounts.models import UserProfile
import random
from decimal import Decimal

class Command(BaseCommand):
    help = 'Create mock data for debugging and testing purposes'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to create mock data...'))
        
        # Create superuser if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_user(
                username='admin',
                email='admin@example.com',
                password='admin123',
                is_staff=True,
                is_superuser=True
            )
            self.stdout.write(self.style.SUCCESS(f'Created superuser: admin/admin123'))
        
        # Create regular users
        users_data = [
            {'username': 'john_doe', 'email': 'john@example.com', 'first_name': 'John', 'last_name': 'Doe'},
            {'username': 'jane_smith', 'email': 'jane@example.com', 'first_name': 'Jane', 'last_name': 'Smith'},
            {'username': 'bob_wilson', 'email': 'bob@example.com', 'first_name': 'Bob', 'last_name': 'Wilson'},
            {'username': 'alice_brown', 'email': 'alice@example.com', 'first_name': 'Alice', 'last_name': 'Brown'},
        ]
        
        created_users = []
        for user_data in users_data:
            if not User.objects.filter(username=user_data['username']).exists():
                user = User.objects.create_user(
                    username=user_data['username'],
                    email=user_data['email'],
                    password='password123',
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name']
                )
                created_users.append(user)
                self.stdout.write(f'Created user: {user.username}')
        
        # Create categories
        categories_data = [
            {'name': 'Electronics', 'description': 'Latest electronic devices and gadgets'},
            {'name': 'Clothing', 'description': 'Fashion and apparel for all ages'},
            {'name': 'Books', 'description': 'Books across all genres and subjects'},
            {'name': 'Home & Garden', 'description': 'Everything for your home and garden'},
            {'name': 'Sports', 'description': 'Sports equipment and athletic wear'},
            {'name': 'Toys & Games', 'description': 'Fun toys and games for all ages'},
            {'name': 'Automotive', 'description': 'Car parts and accessories'},
            {'name': 'Health & Beauty', 'description': 'Health products and beauty supplies'},
        ]
        
        created_categories = []
        for cat_data in categories_data:
            if not Category.objects.filter(name=cat_data['name']).exists():
                category = Category.objects.create(
                    name=cat_data['name'],
                    description=cat_data['description']
                )
                created_categories.append(category)
                self.stdout.write(f'Created category: {category.name}')
        
        # Create products
        products_data = [
            # Electronics
            {'name': 'Smartphone X', 'description': 'Latest smartphone with advanced features', 'price': 699.99, 'stock_quantity': 50, 'category': 'Electronics'},
            {'name': 'Laptop Pro', 'description': 'High-performance laptop for work and gaming', 'price': 1299.99, 'stock_quantity': 25, 'category': 'Electronics'},
            {'name': 'Wireless Headphones', 'description': 'Premium wireless headphones with noise cancellation', 'price': 199.99, 'stock_quantity': 100, 'category': 'Electronics'},
            {'name': 'Smart Watch', 'description': 'Feature-rich smartwatch with health tracking', 'price': 299.99, 'stock_quantity': 75, 'category': 'Electronics'},
            
            # Clothing
            {'name': 'Classic T-Shirt', 'description': 'Comfortable cotton t-shirt in various colors', 'price': 24.99, 'stock_quantity': 200, 'category': 'Clothing'},
            {'name': 'Denim Jeans', 'description': 'High-quality denim jeans for everyday wear', 'price': 79.99, 'stock_quantity': 150, 'category': 'Clothing'},
            {'name': 'Winter Jacket', 'description': 'Warm and stylish winter jacket', 'price': 149.99, 'stock_quantity': 80, 'category': 'Clothing'},
            {'name': 'Running Shoes', 'description': 'Comfortable running shoes for athletes', 'price': 89.99, 'stock_quantity': 120, 'category': 'Clothing'},
            
            # Books
            {'name': 'The Great Adventure', 'description': 'An exciting adventure novel for all ages', 'price': 19.99, 'stock_quantity': 300, 'category': 'Books'},
            {'name': 'Programming Guide', 'description': 'Comprehensive guide to modern programming', 'price': 49.99, 'stock_quantity': 100, 'category': 'Books'},
            {'name': 'Cookbook Deluxe', 'description': 'Collection of delicious recipes from around the world', 'price': 34.99, 'stock_quantity': 150, 'category': 'Books'},
            {'name': 'History of Science', 'description': 'Fascinating journey through scientific discoveries', 'price': 29.99, 'stock_quantity': 80, 'category': 'Books'},
            
            # Home & Garden
            {'name': 'Garden Tool Set', 'description': 'Complete set of essential garden tools', 'price': 89.99, 'stock_quantity': 60, 'category': 'Home & Garden'},
            {'name': 'Kitchen Mixer', 'description': 'Professional kitchen mixer for baking enthusiasts', 'price': 199.99, 'stock_quantity': 40, 'category': 'Home & Garden'},
            {'name': 'LED Desk Lamp', 'description': 'Modern LED desk lamp with adjustable brightness', 'price': 59.99, 'stock_quantity': 90, 'category': 'Home & Garden'},
            {'name': 'Plant Pot Set', 'description': 'Beautiful ceramic plant pots in various sizes', 'price': 39.99, 'stock_quantity': 120, 'category': 'Home & Garden'},
            
            # Sports
            {'name': 'Basketball', 'description': 'Official size basketball for indoor and outdoor use', 'price': 29.99, 'stock_quantity': 100, 'category': 'Sports'},
            {'name': 'Yoga Mat', 'description': 'Premium yoga mat for comfortable practice', 'price': 44.99, 'stock_quantity': 150, 'category': 'Sports'},
            {'name': 'Tennis Racket', 'description': 'Professional tennis racket for serious players', 'price': 129.99, 'stock_quantity': 60, 'category': 'Sports'},
            {'name': 'Fitness Tracker', 'description': 'Advanced fitness tracker with heart rate monitor', 'price': 89.99, 'stock_quantity': 80, 'category': 'Sports'},
            
            # Toys & Games
            {'name': 'Board Game Set', 'description': 'Family board game collection for all ages', 'price': 39.99, 'stock_quantity': 80, 'category': 'Toys & Games'},
            {'name': 'Remote Control Car', 'description': 'High-speed remote control car with rechargeable battery', 'price': 79.99, 'stock_quantity': 60, 'category': 'Toys & Games'},
            {'name': 'Puzzle Collection', 'description': 'Assorted puzzles from 100 to 1000 pieces', 'price': 24.99, 'stock_quantity': 120, 'category': 'Toys & Games'},
            
            # Automotive
            {'name': 'Car Phone Mount', 'description': 'Universal car phone holder for safe navigation', 'price': 19.99, 'stock_quantity': 200, 'category': 'Automotive'},
            {'name': 'LED Light Strip', 'description': 'Customizable LED strip for car interior', 'price': 34.99, 'stock_quantity': 150, 'category': 'Automotive'},
            
            # Health & Beauty
            {'name': 'Skincare Set', 'description': 'Complete skincare routine kit', 'price': 89.99, 'stock_quantity': 100, 'category': 'Health & Beauty'},
            {'name': 'Hair Dryer Pro', 'description': 'Professional hair dryer with multiple settings', 'price': 129.99, 'stock_quantity': 75, 'category': 'Health & Beauty'},
        ]
        
        created_products = []
        for prod_data in products_data:
            if not Product.objects.filter(name=prod_data['name']).exists():
                category = Category.objects.get(name=prod_data['category'])
                # Use admin user as the creator for all products
                admin_user = User.objects.get(username='admin')
                product = Product.objects.create(
                    name=prod_data['name'],
                    description=prod_data['description'],
                    price=prod_data['price'],
                    stock_quantity=prod_data['stock_quantity'],
                    category=category,
                    created_by=admin_user
                )
                created_products.append(product)
                self.stdout.write(f'Created product: {product.name} - ${product.price}')
        
        # Create user profiles for regular users
        for user in created_users:
            if not hasattr(user, 'profile'):
                profile = UserProfile.objects.create(
                    user=user,
                    phone=f'+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}',
                    address=f'{random.randint(100, 9999)} {random.choice(["Main St", "Oak Ave", "Pine Rd", "Elm St"])}',
                    city=random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']),
                    state=random.choice(['NY', 'CA', 'IL', 'TX', 'AZ']),
                    zip_code=f'{random.randint(10000, 99999)}',
                    country='USA'
                )
                self.stdout.write(f'Created profile for user: {user.username}')
        
        self.stdout.write(self.style.SUCCESS('\n=== Mock Data Creation Complete ==='))
        self.stdout.write(f'✅ Created {len(created_users)} users')
        self.stdout.write(f'✅ Created {len(created_categories)} categories')
        self.stdout.write(f'✅ Created {len(created_products)} products (now 30 total products!)')
        self.stdout.write(f'✅ Created user profiles')
        
        self.stdout.write(self.style.SUCCESS('\n=== Login Credentials ==='))
        self.stdout.write('Admin: admin/admin123')
        self.stdout.write('Regular Users: username/password123')
        self.stdout.write('Example: john_doe/password123')
        
        self.stdout.write(self.style.SUCCESS('\nYou can now test the API with this sample data!'))
