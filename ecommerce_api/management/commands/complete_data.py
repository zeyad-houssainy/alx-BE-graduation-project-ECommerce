from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from decimal import Decimal
import random
from categories.models import Category
from products.models import Product, ProductReview
from accounts.models import Wishlist

class Command(BaseCommand):
    help = 'Complete data generation by adding wishlists and final products'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('Completing data generation...')
        )
        
        # Get existing data
        users = list(User.objects.all())
        products = list(Product.objects.all())
        categories = list(Category.objects.all())
        
        self.stdout.write(f'Found {len(users)} users, {len(products)} products, {len(categories)} categories')
        
        # Create wishlists for all users
        self.create_wishlists(users, products)
        
        # Add a few more products to reach exactly 500
        self.add_more_products(categories, users, products)
        
        # Add a few more reviews to reach 1000
        self.add_more_reviews(products, users)
        
        self.stdout.write(
            self.style.SUCCESS('Data generation completed successfully!')
        )

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

    def add_more_products(self, categories, users, existing_products):
        """Add more products to reach exactly 500"""
        current_count = len(existing_products)
        target_count = 500
        
        if current_count >= target_count:
            self.stdout.write(f'Already have {current_count} products, no need to add more')
            return
        
        needed = target_count - current_count
        self.stdout.write(f'Adding {needed} more products...')
        
        # Product templates for additional products
        additional_templates = [
            ('Wireless Earbuds', 'Premium wireless earbuds with noise cancellation', 199.99, 60),
            ('Smart Home Hub', 'Central hub for smart home devices', 149.99, 40),
            ('Fitness Tracker', 'Advanced fitness and health monitoring', 89.99, 80),
            ('Portable Charger', 'High-capacity portable power bank', 49.99, 120),
            ('Bluetooth Keyboard', 'Wireless mechanical keyboard', 129.99, 35),
            ('USB-C Hub', 'Multi-port USB-C adapter', 39.99, 90),
            ('Wireless Mouse', 'Ergonomic wireless gaming mouse', 79.99, 70),
            ('Monitor Stand', 'Adjustable monitor mount', 89.99, 45),
            ('Cable Organizer', 'Cable management solution', 19.99, 150),
            ('Desk Lamp', 'LED desk lamp with adjustable brightness', 59.99, 55),
        ]
        
        products_created = 0
        for name, description, price, stock in additional_templates:
            for i in range(max(1, needed // len(additional_templates))):
                if products_created >= needed:
                    break
                    
                product = Product.objects.create(
                    name=f'{name} {i+1}',
                    slug=slugify(f'{name} {i+1}'),
                    description=f'{description} - Model {i+1}',
                    price=Decimal(str(price + random.uniform(-20, 20))),
                    category=random.choice(categories),
                    stock_quantity=random.randint(0, stock),
                    featured=random.choice([True, False]),
                    created_by=random.choice(users)
                )
                products_created += 1
                
                if products_created % 10 == 0:
                    self.stdout.write(f'Created {products_created} additional products...')
        
        self.stdout.write(f'Added {products_created} more products. Total: {Product.objects.count()}')

    def add_more_reviews(self, products, users):
        """Add more reviews to reach 1000"""
        current_count = ProductReview.objects.count()
        target_count = 1000
        
        if current_count >= target_count:
            self.stdout.write(f'Already have {current_count} reviews, no need to add more')
            return
        
        needed = target_count - current_count
        self.stdout.write(f'Adding {needed} more reviews...')
        
        for i in range(needed):
            product = random.choice(products)
            user = random.choice(users)
            
            # Avoid duplicate reviews
            if not ProductReview.objects.filter(product=product, user=user).exists():
                rating = random.choices([1, 2, 3, 4, 5], weights=[0.05, 0.1, 0.15, 0.3, 0.4])[0]
                
                review = ProductReview.objects.create(
                    product=product,
                    user=user,
                    rating=rating,
                    comment=f'Additional review {i+1}: This is a sample review for testing purposes.'
                )
                
                if i % 50 == 0:
                    self.stdout.write(f'Created {i} additional reviews...')
        
        self.stdout.write(f'Added {needed} more reviews. Total: {ProductReview.objects.count()}')
