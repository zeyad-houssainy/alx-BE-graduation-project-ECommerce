from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from decimal import Decimal
import random
from faker import Faker
from categories.models import Category
from products.models import Product
from accounts.models import UserProfile

class Command(BaseCommand):
    help = 'Generate large dataset with 500 products and 200 users for monitoring'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=200,
            help='Number of users to create (default: 200)'
        )
        parser.add_argument(
            '--products',
            type=int,
            default=500,
            help='Number of products to create (default: 500)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before generating new data'
        )

    def handle(self, *args, **options):
        fake = Faker()
        
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            Product.objects.all().delete()
            UserProfile.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()
            self.stdout.write('Existing data cleared.')
        
        # Create categories if they don't exist
        categories = self.create_categories()
        
        # Create users
        users = self.create_users(options['users'], fake)
        
        # Create products
        products = self.create_products(options['products'], categories, users, fake)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'✅ Large dataset generated successfully!\n'
                f'📊 Summary:\n'
                f'   - Categories: {len(categories)}\n'
                f'   - Users: {len(users)}\n'
                f'   - Products: {len(products)}\n\n'
                f'🔗 You can now:\n'
                f'   - Visit: http://127.0.0.1:8000/api/\n'
                f'   - Browse products: http://127.0.0.1:8000/api/products/\n'
                f'   - View categories: http://127.0.0.1:8000/api/categories/\n'
                f'   - Login to admin: http://127.0.0.1:8000/admin/ (admin/admin)\n'
                f'   - Test pagination: http://127.0.0.1:8000/api/products/?page=1&page_size=20'
            )
        )

    def create_categories(self):
        """Create comprehensive product categories"""
        categories = []
        category_data = [
            ('Electronics', 'Electronic devices and accessories'),
            ('Clothing', 'Apparel and fashion items'),
            ('Home & Garden', 'Home improvement and garden supplies'),
            ('Sports', 'Sports equipment and athletic gear'),
            ('Books', 'Books and educational materials'),
            ('Beauty', 'Beauty and personal care products'),
            ('Automotive', 'Automotive parts and accessories'),
            ('Toys & Games', 'Toys, games, and entertainment'),
            ('Health & Wellness', 'Health and wellness products'),
            ('Food & Beverages', 'Food and beverage items'),
            ('Jewelry', 'Jewelry and accessories'),
            ('Pet Supplies', 'Pet food and supplies'),
            ('Office Supplies', 'Office and stationery items'),
            ('Baby & Kids', 'Baby and children products'),
            ('Outdoor & Camping', 'Outdoor and camping gear'),
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

    def create_users(self, num_users, fake):
        """Create sample users"""
        users = []
        
        # Create admin user if not exists
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_active': True,
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin_user.set_password('admin')
            admin_user.save()
            UserProfile.objects.create(user=admin_user)
            self.stdout.write('Created admin user: admin/admin')
        users.append(admin_user)
        
        # Create regular users
        for i in range(num_users - 1):  # -1 because we already have admin
            username = fake.unique.user_name()
            email = fake.unique.email()
            first_name = fake.first_name()
            last_name = fake.last_name()
            
            user = User.objects.create(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                is_active=random.choice([True, True, True, False]),  # 75% active
                is_staff=random.choice([True, False, False, False, False]),  # 20% staff
            )
            user.set_password('password123')
            user.save()
            
            # Update user profile (signal creates it automatically)
            profile = user.profile
            profile.phone_number = fake.phone_number()[:20]
            profile.address = fake.address()
            profile.date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=80)
            profile.save()
            
            users.append(user)
            
            if (i + 1) % 50 == 0:
                self.stdout.write(f'Created {i + 1} users...')
        
        self.stdout.write(f'Created {len(users)} users total')
        return users

    def create_products(self, num_products, categories, users, fake):
        """Create sample products"""
        products = []
        
        # Product templates for different categories
        product_templates = {
            'Electronics': [
                ('Smartphone', 'Latest smartphone with advanced features', 299.99, 999.99),
                ('Laptop', 'High-performance laptop for work and gaming', 599.99, 2499.99),
                ('Tablet', 'Portable tablet for entertainment and work', 199.99, 899.99),
                ('Headphones', 'Wireless noise-canceling headphones', 49.99, 299.99),
                ('Smartwatch', 'Fitness and health monitoring smartwatch', 99.99, 399.99),
                ('Camera', 'Digital camera for photography enthusiasts', 199.99, 1299.99),
                ('Speaker', 'Bluetooth portable speaker', 29.99, 199.99),
                ('Gaming Console', 'Next-generation gaming console', 299.99, 499.99),
            ],
            'Clothing': [
                ('T-Shirt', 'Comfortable cotton t-shirt', 9.99, 29.99),
                ('Jeans', 'Classic blue jeans', 29.99, 89.99),
                ('Dress', 'Elegant dress for special occasions', 39.99, 199.99),
                ('Sneakers', 'Comfortable athletic sneakers', 49.99, 149.99),
                ('Jacket', 'Warm winter jacket', 59.99, 299.99),
                ('Hoodie', 'Cozy hooded sweatshirt', 24.99, 79.99),
                ('Suit', 'Professional business suit', 199.99, 599.99),
                ('Socks', 'Comfortable cotton socks', 4.99, 19.99),
            ],
            'Home & Garden': [
                ('Garden Tool Set', 'Essential tools for gardening', 29.99, 149.99),
                ('Furniture', 'Modern home furniture', 99.99, 899.99),
                ('Kitchen Appliance', 'Essential kitchen appliance', 49.99, 299.99),
                ('Lighting', 'Modern LED lighting solution', 19.99, 199.99),
                ('Decor', 'Home decoration item', 9.99, 99.99),
                ('Storage', 'Organizational storage solution', 14.99, 149.99),
                ('Bedding', 'Comfortable bedding set', 29.99, 199.99),
                ('Bathroom Accessory', 'Bathroom organization item', 4.99, 49.99),
            ],
            'Sports': [
                ('Basketball', 'Official size basketball', 19.99, 49.99),
                ('Tennis Racket', 'Professional tennis racket', 39.99, 199.99),
                ('Yoga Mat', 'Premium yoga mat', 19.99, 79.99),
                ('Running Shoes', 'High-performance running shoes', 59.99, 199.99),
                ('Gym Equipment', 'Home gym equipment', 99.99, 599.99),
                ('Swimming Gear', 'Swimming accessories', 14.99, 89.99),
                ('Cycling Helmet', 'Safety cycling helmet', 29.99, 149.99),
                ('Fitness Tracker', 'Activity and health monitor', 49.99, 299.99),
            ],
            'Books': [
                ('Fiction Novel', 'Bestselling fiction novel', 9.99, 24.99),
                ('Programming Guide', 'Technical programming book', 19.99, 59.99),
                ('Cookbook', 'Recipe collection cookbook', 14.99, 39.99),
                ('Self-Help Book', 'Personal development guide', 12.99, 29.99),
                ('Children\'s Book', 'Educational children\'s book', 7.99, 19.99),
                ('Academic Textbook', 'Educational textbook', 29.99, 99.99),
                ('Biography', 'Famous person biography', 11.99, 34.99),
                ('Travel Guide', 'Travel destination guide', 13.99, 29.99),
            ],
            'Beauty': [
                ('Face Cream', 'Anti-aging face cream', 19.99, 89.99),
                ('Shampoo', 'Hair care shampoo', 8.99, 39.99),
                ('Makeup Kit', 'Professional makeup collection', 24.99, 149.99),
                ('Perfume', 'Luxury fragrance', 29.99, 199.99),
                ('Skincare Set', 'Complete skincare routine', 34.99, 179.99),
                ('Hair Styling Tool', 'Professional hair styling tool', 39.99, 199.99),
                ('Nail Polish', 'Long-lasting nail polish', 4.99, 24.99),
                ('Sunscreen', 'Broad spectrum sunscreen', 12.99, 49.99),
            ],
            'Automotive': [
                ('Car Accessory', 'Essential car accessory', 9.99, 99.99),
                ('Motor Oil', 'High-quality motor oil', 14.99, 49.99),
                ('Car Care Kit', 'Complete car care solution', 19.99, 149.99),
                ('Tire Gauge', 'Digital tire pressure gauge', 4.99, 29.99),
                ('Car Cover', 'Protective car cover', 29.99, 199.99),
                ('Floor Mats', 'Custom car floor mats', 19.99, 89.99),
                ('Car Charger', 'USB car charger', 7.99, 39.99),
                ('Windshield Wiper', 'Replacement wiper blades', 8.99, 34.99),
            ],
            'Toys & Games': [
                ('Board Game', 'Family board game', 14.99, 49.99),
                ('Puzzle', 'Educational puzzle', 9.99, 39.99),
                ('Action Figure', 'Collectible action figure', 12.99, 59.99),
                ('Building Blocks', 'Creative building set', 19.99, 99.99),
                ('Video Game', 'Popular video game', 29.99, 69.99),
                ('Art Supplies', 'Creative art kit', 7.99, 49.99),
                ('Remote Control Car', 'RC car for kids', 24.99, 149.99),
                ('Doll Set', 'Collectible doll collection', 19.99, 89.99),
            ],
            'Health & Wellness': [
                ('Vitamins', 'Daily vitamin supplement', 12.99, 49.99),
                ('Protein Powder', 'Whey protein supplement', 19.99, 79.99),
                ('Fitness Band', 'Resistance training band', 7.99, 29.99),
                ('Massage Tool', 'Therapeutic massage device', 14.99, 89.99),
                ('Essential Oils', 'Natural essential oil set', 9.99, 49.99),
                ('Meditation App', 'Guided meditation app', 4.99, 19.99),
                ('Water Bottle', 'Insulated water bottle', 12.99, 39.99),
                ('Sleep Aid', 'Natural sleep supplement', 8.99, 34.99),
            ],
            'Food & Beverages': [
                ('Organic Snack', 'Healthy organic snack', 3.99, 19.99),
                ('Coffee Beans', 'Premium coffee beans', 8.99, 39.99),
                ('Tea Collection', 'Assorted tea collection', 6.99, 29.99),
                ('Protein Bar', 'High-protein nutrition bar', 1.99, 4.99),
                ('Superfood Powder', 'Nutrient-rich superfood', 14.99, 59.99),
                ('Cooking Oil', 'Premium cooking oil', 4.99, 24.99),
                ('Spice Set', 'Gourmet spice collection', 9.99, 39.99),
                ('Chocolate', 'Premium chocolate bar', 2.99, 12.99),
            ],
            'Jewelry': [
                ('Necklace', 'Elegant necklace design', 29.99, 299.99),
                ('Ring', 'Beautiful ring design', 49.99, 599.99),
                ('Earrings', 'Stylish earring set', 19.99, 199.99),
                ('Bracelet', 'Charm bracelet', 24.99, 149.99),
                ('Watch', 'Luxury timepiece', 99.99, 999.99),
                ('Anklet', 'Delicate anklet', 14.99, 79.99),
                ('Brooch', 'Vintage brooch', 34.99, 199.99),
                ('Cufflinks', 'Elegant cufflinks', 39.99, 249.99),
            ],
            'Pet Supplies': [
                ('Pet Food', 'Premium pet food', 9.99, 49.99),
                ('Pet Toy', 'Interactive pet toy', 4.99, 24.99),
                ('Pet Bed', 'Comfortable pet bed', 19.99, 99.99),
                ('Pet Grooming Kit', 'Complete grooming set', 14.99, 79.99),
                ('Pet Carrier', 'Travel pet carrier', 24.99, 149.99),
                ('Pet Collar', 'Adjustable pet collar', 7.99, 39.99),
                ('Pet Treats', 'Healthy pet treats', 3.99, 19.99),
                ('Pet Leash', 'Durable pet leash', 9.99, 49.99),
            ],
            'Office Supplies': [
                ('Notebook', 'Premium notebook', 4.99, 19.99),
                ('Pen Set', 'Professional pen collection', 7.99, 39.99),
                ('Desk Organizer', 'Office desk organizer', 12.99, 59.99),
                ('Printer Paper', 'High-quality printer paper', 5.99, 24.99),
                ('Stapler', 'Heavy-duty stapler', 8.99, 34.99),
                ('Whiteboard', 'Office whiteboard', 19.99, 99.99),
                ('File Cabinet', 'Storage file cabinet', 49.99, 299.99),
                ('Calculator', 'Scientific calculator', 9.99, 49.99),
            ],
            'Baby & Kids': [
                ('Baby Food', 'Organic baby food', 2.99, 9.99),
                ('Diapers', 'Premium baby diapers', 19.99, 49.99),
                ('Baby Toy', 'Educational baby toy', 7.99, 34.99),
                ('Kids Clothing', 'Comfortable kids clothing', 9.99, 39.99),
                ('Baby Bottle', 'BPA-free baby bottle', 4.99, 19.99),
                ('Kids Book', 'Educational children\'s book', 5.99, 19.99),
                ('Baby Monitor', 'Digital baby monitor', 49.99, 199.99),
                ('Kids Shoes', 'Comfortable kids shoes', 14.99, 59.99),
            ],
            'Outdoor & Camping': [
                ('Tent', 'Weather-resistant tent', 49.99, 299.99),
                ('Sleeping Bag', 'Warm sleeping bag', 29.99, 149.99),
                ('Camping Stove', 'Portable camping stove', 19.99, 99.99),
                ('Backpack', 'Hiking backpack', 24.99, 199.99),
                ('Water Filter', 'Portable water filter', 14.99, 79.99),
                ('Camping Chair', 'Folding camping chair', 12.99, 59.99),
                ('Flashlight', 'LED camping flashlight', 7.99, 39.99),
                ('First Aid Kit', 'Emergency first aid kit', 9.99, 49.99),
            ],
        }
        
        for i in range(num_products):
            # Select random category
            category = random.choice(categories)
            category_name = category.name
            
            # Get product template for this category
            if category_name in product_templates:
                templates = product_templates[category_name]
            else:
                templates = product_templates['Electronics']  # fallback
            
            # Select random template
            name_template, desc_template, min_price, max_price = random.choice(templates)
            
            # Generate unique product name
            product_name = f"{name_template} {fake.word().title()} {fake.word().title()}"
            
            # Generate price within range
            price = Decimal(str(round(random.uniform(min_price, max_price), 2)))
            
            # Generate stock quantity
            stock_quantity = random.randint(0, 200)
            
            # Create product
            product = Product.objects.create(
                name=product_name,
                slug=slugify(product_name),
                description=f"{desc_template} - {fake.sentence()}",
                price=price,
                category=category,
                stock_quantity=stock_quantity,
                is_active=random.choice([True, True, True, False]),  # 75% active
                created_by=random.choice(users)
            )
            
            products.append(product)
            
            if (i + 1) % 100 == 0:
                self.stdout.write(f'Created {i + 1} products...')
        
        self.stdout.write(f'Created {len(products)} products total')
        return products
