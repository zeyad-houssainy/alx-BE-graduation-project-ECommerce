from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.db import transaction
from accounts.serializers import UserCreateSerializer
from django.utils import timezone
from django.core.management import call_command
from django.views.decorators.csrf import csrf_exempt
import json


def home(request):
    """Home page view"""
    return render(request, 'home.html')


def api_root(request):
    """API root endpoint showing available endpoints with page header"""
    return render(request, 'api_root.html')


def user_login(request):
    """User login view for templates"""
    if request.user.is_authenticated:
        next_url = request.GET.get('next', 'crud-dashboard')
        return redirect(next_url)
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f'Welcome back, {user.username}!')
                    next_url = request.GET.get('next', 'crud-dashboard')
                    return redirect(next_url)
                else:
                    messages.error(request, 'Your account is disabled. Please contact an administrator.')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please provide both username and password.')
    
    return render(request, 'auth/login.html')


def user_logout(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')


def user_register(request):
    """User registration view for templates"""
    if request.user.is_authenticated:
        return redirect('crud-dashboard')
    
    if request.method == 'POST':
        try:
            # Get form data
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            password_confirm = request.POST.get('password_confirm')
            first_name = request.POST.get('first_name', '')
            last_name = request.POST.get('last_name', '')
            
            # Validate required fields
            if not all([username, email, password, password_confirm]):
                messages.error(request, 'All fields are required.')
                return render(request, 'auth/register.html')
            
            # Validate password confirmation
            if password != password_confirm:
                messages.error(request, 'Passwords do not match.')
                return render(request, 'auth/register.html')
            
            # Check if username already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists.')
                return render(request, 'auth/register.html')
            
            # Check if email already exists
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists.')
                return render(request, 'auth/register.html')
            
            # Create user
            with transaction.atomic():
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )
                
                # Profile is created automatically by signal
                messages.success(request, f'Account created successfully! Welcome, {user.username}!')
                return redirect('user-login')
                
        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
    
    return render(request, 'auth/register.html')


@login_required
def profile(request):
    """User profile view"""
    return render(request, 'auth/profile.html')


def documentation(request):
    """API documentation view"""
    return render(request, 'documentation.html')


def healthcheck(request):
    """Healthcheck endpoint for Railway deployment"""
    return JsonResponse({
        'status': 'healthy',
        'message': 'Django E-commerce API is running',
        'timestamp': timezone.now().isoformat()
    })


def create_mock_data(request):
    """Create mock data for debugging purposes"""
    if request.method == 'POST':
        try:
            # Call the management command
            call_command('create_mock_data')
            messages.success(request, 'Mock data created successfully! You can now test the API with sample data.')
            return JsonResponse({'status': 'success', 'message': 'Mock data created successfully!'})
        except Exception as e:
            messages.error(request, f'Error creating mock data: {str(e)}')
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return redirect('home')


def create_mock_users(request):
    """Create mock users for debugging purposes"""
    if request.method == 'POST':
        try:
            # Call the management command
            call_command('create_mock_users')
            messages.success(request, 'Mock users created successfully! You can now test user management features.')
            return JsonResponse({'status': 'success', 'message': 'Mock users created successfully!'})
        except Exception as e:
            messages.error(request, f'Error creating mock users: {str(e)}')
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return redirect('home')


def setup_database_mock(request):
    """Complete setup: Create database, run migrations, and create mock data"""
    if request.method == 'POST':
        try:
            import mysql.connector
            from django.conf import settings
            from django.core.management import call_command
            import subprocess
            import sys
            
            response_data = {'status': 'success', 'steps': [], 'message': ''}
            
            # Step 1: Check MySQL connection and create database if needed
            try:
                # Connect to MySQL as root
                connection = mysql.connector.connect(
                    host=settings.DATABASES['default']['HOST'],
                    user=settings.DATABASES['default']['USER'],
                    password=settings.DATABASES['default']['PASSWORD'],
                    port=settings.DATABASES['default']['PORT']
                )
                
                if connection.is_connected():
                    cursor = connection.cursor()
                    
                    # Check if database exists
                    cursor.execute("SHOW DATABASES LIKE %s", (settings.DATABASES['default']['NAME'],))
                    db_exists = cursor.fetchone()
                    
                    if not db_exists:
                        # Create database
                        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {settings.DATABASES['default']['NAME']} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                        response_data['steps'].append('✅ Database created successfully')
                    else:
                        response_data['steps'].append('✅ Database already exists')
                    
                    cursor.close()
                    connection.close()
                    
            except Exception as e:
                response_data['status'] = 'error'
                response_data['message'] = f'Database setup failed: {str(e)}'
                return JsonResponse(response_data)
            
            # Step 2: Run migrations
            try:
                call_command('migrate', verbosity=0)
                response_data['steps'].append('✅ Database migrations applied')
            except Exception as e:
                response_data['status'] = 'error'
                response_data['message'] = f'Migration failed: {str(e)}'
                return JsonResponse(response_data)
            
            # Step 3: Create mock data
            try:
                call_command('create_mock_data', verbosity=0)
                response_data['steps'].append('✅ Mock data created')
            except Exception as e:
                response_data['steps'].append(f'⚠️ Mock data creation failed: {str(e)}')
            
            # Step 4: Create mock users
            try:
                call_command('create_mock_users', verbosity=0)
                response_data['steps'].append('✅ Mock users created')
            except Exception as e:
                response_data['steps'].append(f'⚠️ Mock users creation failed: {str(e)}')
            
            response_data['message'] = 'Database setup completed successfully!'
            return JsonResponse(response_data)
            
        except Exception as e:
            return JsonResponse({
                'status': 'error', 
                'message': f'Setup failed: {str(e)}'
            })
    
    return redirect('home')
