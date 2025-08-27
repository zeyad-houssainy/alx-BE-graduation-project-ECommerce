from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.urls import reverse
from products.models import Product
from categories.models import Category
from accounts.models import UserProfile
import json


def is_staff_or_superuser(user):
    """Check if user is staff or superuser"""
    return user.is_staff or user.is_superuser


def login_required_custom(function):
    """Custom login required decorator that redirects to login with next parameter"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Please log in to access this page.')
            return redirect(f"{reverse('user-login')}?next={request.path}")
        return function(request, *args, **kwargs)
    return wrapper


@login_required_custom
def crud_dashboard(request):
    """Main CRUD dashboard view"""
    context = {
        'total_products': Product.objects.count(),
        'total_categories': Category.objects.count(),
        'total_users': User.objects.count(),
        'low_stock_count': Product.objects.filter(stock_quantity__lt=10, is_active=True).count(),
        'recent_products': Product.objects.select_related('category').order_by('-created_at')[:5],
        'recent_categories': Category.objects.annotate(product_count=Count('products')).order_by('-created_at')[:5],
        'recent_users': User.objects.select_related('profile').order_by('-date_joined')[:5],
    }
    return render(request, 'crud_dashboard.html', context)


@login_required_custom
def crud_products(request):
    """Products CRUD view"""
    action = request.GET.get('action', '')
    product_id = request.GET.get('id')
    
    if action == 'create':
        return render_products_create_form(request)
    elif action == 'edit' and product_id:
        return render_products_edit_form(request, product_id)
    elif action == 'delete' and product_id:
        return delete_product(request, product_id)
    else:
        return render_products_list(request)


@login_required_custom
def render_products_create_form(request):
    """Render product creation form"""
    if request.method == 'POST':
        return create_product(request)
    
    context = {
        'action': 'create',
        'categories': Category.objects.filter(is_active=True),
        'product': None
    }
    return render(request, 'crud_products.html', context)


@login_required_custom
def render_products_edit_form(request, product_id):
    """Render product edit form"""
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        return update_product(request, product)
    
    context = {
        'action': 'edit',
        'product': product,
        'categories': Category.objects.filter(is_active=True)
    }
    return render(request, 'crud_products.html', context)


@login_required_custom
def render_products_list(request):
    """Render products list with search and filtering"""
    # Get search and filter parameters
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    stock_status = request.GET.get('stock_status', '')
    
    # Base queryset
    products = Product.objects.select_related('category', 'created_by').filter(is_active=True)
    
    # Apply search filter
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )
    
    # Apply category filter
    if category_filter:
        products = products.filter(category_id=category_filter)
    
    # Apply stock status filter
    if stock_status == 'in_stock':
        products = products.filter(stock_quantity__gt=0)
    elif stock_status == 'low_stock':
        products = products.filter(stock_quantity__lt=10, stock_quantity__gt=0)
    elif stock_status == 'out_of_stock':
        products = products.filter(stock_quantity=0)
    
    # Pagination
    paginator = Paginator(products, 12)  # 12 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'products': page_obj,
        'categories': Category.objects.filter(is_active=True),
        'total_products': products.count(),
        'active_products': products.filter(is_active=True).count(),
        'action': 'list'
    }
    return render(request, 'crud_products.html', context)


@require_http_methods(["POST"])
@login_required_custom
def create_product(request):
    """Create a new product"""
    try:
        # Get form data
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category_id = request.POST.get('category')
        stock_quantity = request.POST.get('stock_quantity')
        is_active = request.POST.get('is_active') == 'True'
        
        # Validate required fields
        if not all([name, description, price, category_id, stock_quantity]):
            messages.error(request, 'All required fields must be filled.')
            return redirect('crud-products')
        
        # Get category
        category = get_object_or_404(Category, id=category_id)
        
        # Create product
        product = Product.objects.create(
            name=name,
            description=description,
            price=price,
            category=category,
            stock_quantity=stock_quantity,
            is_active=is_active,
            created_by=request.user
        )
        
        # Handle image upload
        if 'image' in request.FILES:
            product.image = request.FILES['image']
            product.save()
        
        messages.success(request, f'Product "{product.name}" created successfully!')
        return redirect('crud-products')
        
    except Exception as e:
        messages.error(request, f'Error creating product: {str(e)}')
        return redirect('crud-products')


@require_http_methods(["POST"])
@login_required_custom
def update_product(request, product):
    """Update an existing product"""
    try:
        # Get form data
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        category_id = request.POST.get('category')
        product.stock_quantity = request.POST.get('stock_quantity')
        product.is_active = request.POST.get('is_active') == 'True'
        
        # Update category if changed
        if category_id:
            category = get_object_or_404(Category, id=category_id)
            product.category = category
        
        # Handle image upload
        if 'image' in request.FILES:
            product.image = request.FILES['image']
        
        product.save()
        
        messages.success(request, f'Product "{product.name}" updated successfully!')
        return redirect('crud-products')
        
    except Exception as e:
        messages.error(request, f'Error updating product: {str(e)}')
        return redirect('crud-products')


@login_required_custom
def delete_product(request, product_id):
    """Delete a product (soft delete)"""
    try:
        product = get_object_or_404(Product, id=product_id)
        product.is_active = False
        product.save()
        messages.success(request, f'Product "{product.name}" deleted successfully!')
    except Exception as e:
        messages.error(request, f'Error deleting product: {str(e)}')
    
    return redirect('crud-products')


@login_required_custom
def crud_categories(request):
    """Categories CRUD view"""
    action = request.GET.get('action', '')
    category_id = request.GET.get('id')
    
    if action == 'create':
        return render_categories_create_form(request)
    elif action == 'edit' and category_id:
        return render_categories_edit_form(request, category_id)
    elif action == 'delete' and category_id:
        return delete_category(request, category_id)
    else:
        return render_categories_list(request)


@login_required_custom
def render_categories_create_form(request):
    """Render category creation form"""
    if request.method == 'POST':
        return create_category(request)
    
    context = {
        'action': 'create',
        'category': None
    }
    return render(request, 'crud_categories.html', context)


@login_required_custom
def render_categories_edit_form(request, category_id):
    """Render category edit form"""
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        return update_category(request, category)
    
    context = {
        'action': 'edit',
        'category': category
    }
    return render(request, 'crud_categories.html', context)


@login_required_custom
def render_categories_list(request):
    """Render categories list with search and filtering"""
    # Get search and filter parameters
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    
    # Base queryset
    categories = Category.objects.annotate(product_count=Count('products'))
    
    # Apply search filter
    if search_query:
        categories = categories.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Apply status filter
    if status_filter == 'active':
        categories = categories.filter(is_active=True)
    elif status_filter == 'inactive':
        categories = categories.filter(is_active=False)
    
    # Pagination
    paginator = Paginator(categories, 12)  # 12 categories per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'categories': page_obj,
        'total_categories': categories.count(),
        'active_categories': categories.filter(is_active=True).count(),
        'action': 'list'
    }
    return render(request, 'crud_categories.html', context)


@require_http_methods(["POST"])
@login_required_custom
def create_category(request):
    """Create a new category"""
    try:
        # Get form data
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        is_active = request.POST.get('is_active') == 'True'
        
        # Validate required fields
        if not name:
            messages.error(request, 'Category name is required.')
            return redirect('crud-categories')
        
        # Check if category name already exists
        if Category.objects.filter(name=name).exists():
            messages.error(request, 'Category with this name already exists.')
            return redirect('crud-categories')
        
        # Create category
        category = Category.objects.create(
            name=name,
            description=description,
            is_active=is_active
        )
        
        messages.success(request, f'Category "{category.name}" created successfully!')
        return redirect('crud-categories')
        
    except Exception as e:
        messages.error(request, f'Error creating category: {str(e)}')
        return redirect('crud-categories')


@require_http_methods(["POST"])
@login_required_custom
def update_category(request, category):
    """Update an existing category"""
    try:
        # Get form data
        category.name = request.POST.get('name')
        category.description = request.POST.get('description', '')
        category.is_active = request.POST.get('is_active') == 'True'
        
        # Validate required fields
        if not category.name:
            messages.error(request, 'Category name is required.')
            return redirect('crud-categories')
        
        # Check if category name already exists (excluding current category)
        if Category.objects.exclude(id=category.id).filter(name=category.name).exists():
            messages.error(request, 'Category with this name already exists.')
            return redirect('crud-categories')
        
        category.save()
        
        messages.success(request, f'Category "{category.name}" updated successfully!')
        return redirect('crud-categories')
        
    except Exception as e:
        messages.error(request, f'Error updating category: {str(e)}')
        return redirect('crud-categories')


@login_required_custom
def delete_category(request, category_id):
    """Delete a category (soft delete)"""
    try:
        category = get_object_or_404(Category, id=category_id)
        category.is_active = False
        category.save()
        messages.success(request, f'Category "{category.name}" deleted successfully!')
    except Exception as e:
        messages.error(request, f'Error deleting category: {str(e)}')
    
    return redirect('crud-categories')


@login_required_custom
@user_passes_test(is_staff_or_superuser)
def crud_users(request):
    """Users CRUD view - Staff only"""
    action = request.GET.get('action', '')
    user_id = request.GET.get('id')
    
    if action == 'create':
        return render_users_create_form(request)
    elif action == 'edit' and user_id:
        return render_users_edit_form(request, user_id)
    elif action == 'delete' and user_id:
        return delete_user(request, user_id)
    else:
        return render_users_list(request)


@login_required_custom
@user_passes_test(is_staff_or_superuser)
def render_users_create_form(request):
    """Render user creation form - Staff only"""
    if request.method == 'POST':
        return create_user(request)
    
    context = {
        'action': 'create'
    }
    return render(request, 'crud_users.html', context)


@login_required_custom
@user_passes_test(is_staff_or_superuser)
def render_users_edit_form(request, user_id):
    """Render user edit form - Staff only"""
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        return update_user(request, user)
    
    context = {
        'action': 'edit',
        'user': user
    }
    return render(request, 'crud_users.html', context)


@login_required_custom
@user_passes_test(is_staff_or_superuser)
def render_users_list(request):
    """Render users list with search and filtering - Staff only"""
    # Get search and filter parameters
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    role_filter = request.GET.get('role', '')
    
    # Base queryset
    users = User.objects.select_related('profile')
    
    # Apply search filter
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )
    
    # Apply status filter
    if status_filter == 'active':
        users = users.filter(is_active=True)
    elif status_filter == 'inactive':
        users = users.filter(is_active=False)
    elif status_filter == 'staff':
        users = users.filter(is_staff=True)
    elif status_filter == 'superuser':
        users = users.filter(is_superuser=True)
    
    # Apply role filter
    if role_filter == 'user':
        users = users.filter(is_staff=False, is_superuser=False)
    elif role_filter == 'staff':
        users = users.filter(is_staff=True, is_superuser=False)
    elif role_filter == 'admin':
        users = users.filter(is_superuser=True)
    
    # Pagination
    paginator = Paginator(users, 12)  # 12 users per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'users': page_obj,
        'total_users': users.count(),
        'active_users': users.filter(is_active=True).count(),
        'action': 'list'
    }
    return render(request, 'crud_users.html', context)


@require_http_methods(["POST"])
@login_required_custom
@user_passes_test(is_staff_or_superuser)
def create_user(request):
    """Create a new user - Staff only"""
    try:
        # Get form data
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        is_active = request.POST.get('is_active') == 'True'
        is_staff = request.POST.get('is_staff') == 'True'
        is_superuser = request.POST.get('is_superuser') == 'True'
        
        # Validate required fields
        if not all([username, email, password, password_confirm]):
            messages.error(request, 'Username, email, and password are required.')
            return redirect('crud-users')
        
        # Validate password confirmation
        if password != password_confirm:
            messages.error(request, 'Passwords do not match.')
            return redirect('crud-users')
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('crud-users')
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('crud-users')
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_active=is_active,
            is_staff=is_staff,
            is_superuser=is_superuser
        )
        
        # Update profile information
        profile = user.profile
        profile.phone_number = request.POST.get('phone_number', '')
        profile.address = request.POST.get('address', '')
        
        date_of_birth = request.POST.get('date_of_birth')
        if date_of_birth:
            profile.date_of_birth = date_of_birth
        
        profile.save()
        
        messages.success(request, f'User "{user.username}" created successfully!')
        return redirect('crud-users')
        
    except Exception as e:
        messages.error(request, f'Error creating user: {str(e)}')
        return redirect('crud-users')


@require_http_methods(["POST"])
@login_required_custom
@user_passes_test(is_staff_or_superuser)
def update_user(request, user):
    """Update an existing user - Staff only"""
    try:
        # Get form data
        user.email = request.POST.get('email')
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.is_active = request.POST.get('is_active') == 'True'
        user.is_staff = request.POST.get('is_staff') == 'True'
        user.is_superuser = request.POST.get('is_superuser') == 'True'
        
        user.save()
        
        # Update profile information
        profile = user.profile
        profile.phone_number = request.POST.get('phone_number', '')
        profile.address = request.POST.get('address', '')
        
        date_of_birth = request.POST.get('date_of_birth')
        if date_of_birth:
            profile.date_of_birth = date_of_birth
        
        profile.save()
        
        messages.success(request, f'User "{user.username}" updated successfully!')
        return redirect('crud-users')
        
    except Exception as e:
        messages.error(request, f'Error updating user: {str(e)}')
        return redirect('crud-users')


@login_required_custom
@user_passes_test(is_staff_or_superuser)
def delete_user(request, user_id):
    """Delete a user (hard delete) - Staff only"""
    try:
        user = get_object_or_404(User, id=user_id)
        username = user.username
        user.delete()
        messages.success(request, f'User "{username}" deleted successfully!')
    except Exception as e:
        messages.error(request, f'Error deleting user: {str(e)}')
    
    return redirect('crud-users')



