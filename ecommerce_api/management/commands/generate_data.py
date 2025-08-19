from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from decimal import Decimal
import random
from categories.models import Category
from products.models import Product, ProductReview
from accounts.models import UserProfile, Wishlist

class Command(BaseCommand):
    help = 'Generate sample data for the e-commerce project'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('Starting data generation...')
        )
        
        # Create categories
        categories = self.create_categories()
        
        # Create users
        users = self.create_users()
        
        # Create products
        products = self.create_products(categories, users)
        
        # Create reviews
        self.create_reviews(products, users)
        
        # Create wishlists
        self.create_wishlists(users, products)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created:\n'
                f'- {len(categories)} categories\n'
                f'- {len(users)} users\n'
                f'- {len(products)} products\n'
                f'- Reviews and wishlists'
            )
        )

    def create_categories(self):
        """Create product categories"""
        categories = []
        category_data = [
            ('Electronics', 'Electronic devices and gadgets'),
            ('Fashion', 'Clothing and accessories'),
            ('Home & Garden', 'Home improvement and garden items'),
            ('Sports & Outdoors', 'Sports equipment and outdoor gear'),
            ('Books & Media', 'Books, movies, and music'),
            ('Toys & Games', 'Children toys and board games'),
            ('Health & Beauty', 'Health products and beauty items'),
            ('Automotive', 'Car parts and accessories'),
            ('Tools & Hardware', 'DIY tools and hardware'),
            ('Pet Supplies', 'Pet food and accessories'),
        ]
        
        for name, description in category_data:
            category, created = Category.objects.get_or_create(
                name=name,
                defaults={
                    'slug': slugify(name),
                    'description': description
                }
            )
            if created:
                self.stdout.write(f'Created category: {name}')
            else:
                self.stdout.write(f'Category already exists: {name}')
            categories.append(category)
        
        return categories

    def create_users(self):
        """Create user accounts"""
        users = []
        
        # Create admin user if it doesn't exist
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@ecommerce.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin_user.set_password('admin')
            admin_user.save()
            self.stdout.write('Created admin user: admin/admin')
        
        # Create regular users
        for i in range(50):
            username = f'user{i+1}'
            email = f'user{i+1}@example.com'
            
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'password': 'password123',
                    'first_name': f'User{i+1}',
                    'last_name': f'Last{i+1}'
                }
            )
            
            if created:
                user.set_password('password123')
                user.save()
                
                # Update profile
                profile = user.profile
                profile.phone_number = f'+1-555-{str(i+1).zfill(3)}-{str(i+1).zfill(4)}'
                profile.address = f'{i+1} Main Street, City {i+1}'
                profile.save()
                
                if i % 10 == 0:
                    self.stdout.write(f'Created user: {username}')
            else:
                if i % 10 == 0:
                    self.stdout.write(f'User already exists: {username}')
            
            users.append(user)
        
        return users

    def create_products(self, categories, users):
        """Create products"""
        products = []
        
        # Product templates
        product_templates = [
            ('Smartphone X', 'Latest smartphone with advanced features', 599.99, 50),
            ('Laptop Pro', 'Professional laptop for creators', 1299.99, 25),
            ('Gaming Console', 'Next-gen gaming console', 399.99, 60),
            ('Wireless Headphones', 'Premium noise-canceling headphones', 299.99, 40),
            ('Digital Camera', 'Professional camera for photography', 899.99, 20),
            ('Smart Watch', 'Fitness and health tracking watch', 199.99, 75),
            ('Tablet', 'Portable tablet for work and entertainment', 399.99, 35),
            ('Gaming Laptop', 'High-performance gaming laptop', 1499.99, 15),
            ('Bluetooth Speaker', 'Portable wireless speaker', 79.99, 100),
            ('Action Camera', 'Adventure and sports camera', 299.99, 45),
        ]
        
        # Create products from templates
        for name, description, price, stock in product_templates:
            for i in range(50):  # Create 50 of each template
                product = Product.objects.create(
                    name=f'{name} {i+1}',
                    slug=slugify(f'{name} {i+1}'),
                    description=f'{description} - Model {i+1}',
                    price=Decimal(str(price + random.uniform(-50, 50))),
                    category=random.choice(categories),
                    stock_quantity=random.randint(0, stock),
                    featured=random.choice([True, False]),
                    created_by=random.choice(users)
                )
                products.append(product)
                
                if len(products) % 100 == 0:
                    self.stdout.write(f'Created {len(products)} products...')
        
        return products

    def create_reviews(self, products, users):
        """Create product reviews"""
        for i in range(1000):
            product = random.choice(products)
            user = random.choice(users)
            
            # Avoid duplicate reviews
            if not ProductReview.objects.filter(product=product, user=user).exists():
                rating = random.choices([1, 2, 3, 4, 5], weights=[0.05, 0.1, 0.15, 0.3, 0.4])[0]
                
                review = ProductReview.objects.create(
                    product=product,
                    user=user,
                    rating=rating,
                    comment=f'Review {i+1}: This is a sample review for testing purposes.'
                )
                
                if i % 100 == 0:
                    self.stdout.write(f'Created {i} reviews...')

    def create_wishlists(self, users, products):
        """Create wishlists for users"""
        for user in users:
            # Get or create wishlist
            wishlist, created = Wishlist.objects.get_or_create(user=user)
            
            # Add 1-5 random products to each wishlist
            num_products = random.randint(1, 5)
            selected_products = random.sample(list(products), min(num_products, len(products)))
            
            for product in selected_products:
                wishlist.products.add(product)
            
            if created:
                self.stdout.write(f'Created wishlist for {user.username} with {len(selected_products)} products')
            else:
                self.stdout.write(f'Updated wishlist for {user.username} with {len(selected_products)} products')
