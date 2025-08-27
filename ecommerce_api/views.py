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
