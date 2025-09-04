from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import UserProfile
import random

class Command(BaseCommand):
    help = 'Create mock users for testing and debugging purposes'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to create mock users...'))
        
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
        else:
            admin_user = User.objects.get(username='admin')
            self.stdout.write(f'Admin user already exists: admin/admin123')
        
        # Create regular users with more variety
        users_data = [
            # Developers
            {'username': 'john_doe', 'email': 'john@example.com', 'first_name': 'John', 'last_name': 'Doe', 'is_staff': False},
            {'username': 'jane_smith', 'email': 'jane@example.com', 'first_name': 'Jane', 'last_name': 'Smith', 'is_staff': False},
            {'username': 'bob_wilson', 'email': 'bob@example.com', 'first_name': 'Bob', 'last_name': 'Wilson', 'is_staff': False},
            {'username': 'alice_brown', 'email': 'alice@example.com', 'first_name': 'Alice', 'last_name': 'Brown', 'is_staff': False},
            
            # Additional test users
            {'username': 'mike_johnson', 'email': 'mike@example.com', 'first_name': 'Mike', 'last_name': 'Johnson', 'is_staff': False},
            {'username': 'sarah_davis', 'email': 'sarah@example.com', 'first_name': 'Sarah', 'last_name': 'Davis', 'is_staff': False},
            {'username': 'david_miller', 'email': 'david@example.com', 'first_name': 'David', 'last_name': 'Miller', 'is_staff': False},
            {'username': 'lisa_garcia', 'email': 'lisa@example.com', 'first_name': 'Lisa', 'last_name': 'Garcia', 'is_staff': False},
            {'username': 'tom_rodriguez', 'email': 'tom@example.com', 'first_name': 'Tom', 'last_name': 'Rodriguez', 'is_staff': False},
            {'username': 'emma_lee', 'email': 'emma@example.com', 'first_name': 'Emma', 'last_name': 'Lee', 'is_staff': False},
            
            # Staff users for testing different permission levels
            {'username': 'manager_kate', 'email': 'kate@example.com', 'first_name': 'Kate', 'last_name': 'Williams', 'is_staff': True},
            {'username': 'support_alex', 'email': 'alex@example.com', 'first_name': 'Alex', 'last_name': 'Taylor', 'is_staff': True},
        ]
        
        created_users = []
        for user_data in users_data:
            if not User.objects.filter(username=user_data['username']).exists():
                user = User.objects.create_user(
                    username=user_data['username'],
                    email=user_data['email'],
                    password='password123',
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    is_staff=user_data['is_staff']
                )
                created_users.append(user)
                self.stdout.write(f'Created user: {user.username} (Staff: {user.is_staff})')
            else:
                self.stdout.write(f'User already exists: {user_data["username"]}')
        
        # Create user profiles for all users (including existing ones)
        all_users = User.objects.all()
        profiles_created = 0
        
        for user in all_users:
            if not hasattr(user, 'profile'):
                profile = UserProfile.objects.create(
                    user=user,
                    phone=f'+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}',
                    address=f'{random.randint(100, 9999)} {random.choice(["Main St", "Oak Ave", "Pine Rd", "Elm St", "Cedar Ln", "Maple Dr"])}',
                    city=random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose']),
                    state=random.choice(['NY', 'CA', 'IL', 'TX', 'AZ', 'PA', 'FL', 'OH', 'GA', 'NC']),
                    zip_code=f'{random.randint(10000, 99999)}',
                    country='USA'
                )
                profiles_created += 1
                self.stdout.write(f'Created profile for user: {user.username}')
        
        self.stdout.write(self.style.SUCCESS('\n=== Mock Users Creation Complete ==='))
        self.stdout.write(f'✅ Total users in system: {User.objects.count()}')
        self.stdout.write(f'✅ New users created: {len(created_users)}')
        self.stdout.write(f'✅ New profiles created: {profiles_created}')
        
        self.stdout.write(self.style.SUCCESS('\n=== Login Credentials ==='))
        self.stdout.write('Admin: admin/admin123')
        self.stdout.write('Staff Users: manager_kate/password123, support_alex/password123')
        self.stdout.write('Regular Users: username/password123')
        self.stdout.write('Examples: john_doe/password123, mike_johnson/password123')
        
        self.stdout.write(self.style.SUCCESS('\n=== User Types ==='))
        self.stdout.write(f'👑 Superusers: {User.objects.filter(is_superuser=True).count()}')
        self.stdout.write(f'👔 Staff Users: {User.objects.filter(is_staff=True, is_superuser=False).count()}')
        self.stdout.write(f'👤 Regular Users: {User.objects.filter(is_staff=False, is_superuser=False).count()}')
        
        self.stdout.write(self.style.SUCCESS('\nYou can now test user management and authentication features!'))
