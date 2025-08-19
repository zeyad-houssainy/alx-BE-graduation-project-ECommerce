from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import render
from django.db.models import Count, Sum, Avg
from django.utils import timezone
from datetime import timedelta
from accounts.models import UserProfile
from categories.models import Category
from products.models import Product
from django.contrib.auth.models import User


class EcommerceAdminSite(AdminSite):
    site_header = "🛍️ E-Commerce Dashboard"
    site_title = "E-Commerce Admin"
    index_title = "Welcome to E-Commerce Management"
    site_url = "/api/"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(self.dashboard_view), name='dashboard'),
        ]
        return custom_urls + urls

    def dashboard_view(self, request):
        # Get statistics
        total_users = User.objects.count()
        total_products = Product.objects.count()
        total_categories = Category.objects.count()
        active_products = Product.objects.filter(is_active=True).count()
        out_of_stock = Product.objects.filter(stock_quantity=0, is_active=True).count()
        low_stock = Product.objects.filter(stock_quantity__lt=10, stock_quantity__gt=0, is_active=True).count()
        
        # Recent activity
        recent_products = Product.objects.order_by('-created_at')[:5]
        recent_users = User.objects.order_by('-date_joined')[:5]
        
        # Category statistics
        category_stats = Category.objects.annotate(
            product_count=Count('products')
        ).order_by('-product_count')[:10]
        
        # Stock alerts
        stock_alerts = Product.objects.filter(
            stock_quantity__lt=10, 
            is_active=True
        ).order_by('stock_quantity')[:10]
        
        context = {
            'total_users': total_users,
            'total_products': total_products,
            'total_categories': total_categories,
            'active_products': active_products,
            'out_of_stock': out_of_stock,
            'low_stock': low_stock,
            'recent_products': recent_products,
            'recent_users': recent_users,
            'category_stats': category_stats,
            'stock_alerts': stock_alerts,
            'title': 'Dashboard',
            'opts': self._registry[User]._meta,
        }
        return render(request, 'admin/dashboard.html', context)


# Create custom admin site
admin_site = EcommerceAdminSite(name='ecommerce_admin')


# Enhanced User Admin
class EnhancedUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'full_name', 'is_staff', 'is_active', 
                   'profile_picture_preview', 'date_joined', 'last_login')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined', 'last_login')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'profile__phone_number')
    list_per_page = 50
    ordering = ('-date_joined',)
    
    fieldsets = (
        ('Account Information', {
            'fields': ('username', 'email', 'password')
        }),
        ('Personal Information', {
            'fields': ('first_name', 'last_name')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )
    
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip() or "N/A"
    full_name.short_description = 'Full Name'
    
    def profile_picture_preview(self, obj):
        if hasattr(obj, 'profile') and obj.profile.profile_picture:
            return format_html(
                '<img src="{}" style="width: 40px; height: 40px; object-fit: cover; border-radius: 50%; border: 2px solid #ddd;" />',
                obj.profile.profile_picture.url
            )
        return format_html(
            '<div style="width: 40px; height: 40px; background: #f0f0f0; border-radius: 50%; display: flex; align-items: center; justify-content: center; border: 2px solid #ddd;">👤</div>'
        )
    profile_picture_preview.short_description = 'Profile'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('profile')


# Enhanced Category Admin
class EnhancedCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'products_count', 'is_active', 'image_preview', 'created_at')
    list_filter = ('is_active', 'created_at', 'updated_at')
    search_fields = ('name', 'description', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at', 'image_preview', 'products_count_display')
    list_editable = ('is_active',)
    list_per_page = 25
    ordering = ('name',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description')
        }),
        ('Media', {
            'fields': ('image', 'image_preview')
        }),
        ('Statistics', {
            'fields': ('products_count_display',)
        }),
        ('Settings', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def products_count(self, obj):
        count = obj.products.count()
        color = 'green' if count > 0 else 'red'
        return format_html(
            '<span style="color: {}; font-weight: bold; background: {}; padding: 2px 8px; border-radius: 12px; font-size: 12px;">{}</span>',
            'white' if count > 0 else 'white',
            color if count > 0 else '#ff4444',
            count
        )
    products_count.short_description = 'Products'
    
    def products_count_display(self, obj):
        count = obj.products.count()
        active_count = obj.products.filter(is_active=True).count()
        return format_html(
            '<div style="padding: 10px; background: #f8f9fa; border-radius: 5px;">'
            '<strong>Total Products:</strong> {}<br>'
            '<strong>Active Products:</strong> {}<br>'
            '<strong>Inactive Products:</strong> {}'
            '</div>',
            count, active_count, count - active_count
        )
    products_count_display.short_description = 'Product Statistics'
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 80px; height: 80px; object-fit: cover; border-radius: 8px; border: 2px solid #ddd;" />',
                obj.image.url
            )
        return format_html(
            '<div style="width: 80px; height: 80px; background: #f0f0f0; border-radius: 8px; display: flex; align-items: center; justify-content: center; border: 2px solid #ddd;">📁</div>'
        )
    image_preview.short_description = 'Image'
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('products')


# Enhanced Product Admin
class EnhancedProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price_display', 'stock_status', 'stock_quantity', 
                   'is_active', 'image_preview', 'created_by', 'created_at')
    list_filter = ('category', 'is_active', 'created_at', 'updated_at', 'created_by', 'stock_quantity')
    search_fields = ('name', 'description', 'category__name', 'created_by__username')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at', 'image_preview', 'stock_status', 'created_by')
    list_editable = ('is_active', 'stock_quantity')
    list_per_page = 50
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'category')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'stock_quantity', 'stock_status')
        }),
        ('Media', {
            'fields': ('image', 'image_preview')
        }),
        ('Settings', {
            'fields': ('is_active', 'created_by')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['activate_products', 'deactivate_products', 'set_low_stock_alert']
    
    def price_display(self, obj):
        return format_html(
            '<span style="color: #28a745; font-weight: bold;">${}</span>',
            obj.price
        )
    price_display.short_description = 'Price'
    
    def stock_status(self, obj):
        if obj.stock_quantity == 0:
            return format_html(
                '<span style="color: white; background: #dc3545; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">Out of Stock</span>'
            )
        elif obj.stock_quantity < 10:
            return format_html(
                '<span style="color: white; background: #ffc107; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">Low Stock</span>'
            )
        else:
            return format_html(
                '<span style="color: white; background: #28a745; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">In Stock</span>'
            )
    stock_status.short_description = 'Stock Status'
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 80px; height: 80px; object-fit: cover; border-radius: 8px; border: 2px solid #ddd;" />',
                obj.image.url
            )
        return format_html(
            '<div style="width: 80px; height: 80px; background: #f0f0f0; border-radius: 8px; display: flex; align-items: center; justify-content: center; border: 2px solid #ddd;">📦</div>'
        )
    image_preview.short_description = 'Image'
    
    def activate_products(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} products have been activated.')
    activate_products.short_description = "Activate selected products"
    
    def deactivate_products(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} products have been deactivated.')
    deactivate_products.short_description = "Deactivate selected products"
    
    def set_low_stock_alert(self, request, queryset):
        updated = queryset.update(stock_quantity=5)
        self.message_user(request, f'{updated} products have been set to low stock alert (5 items).')
    set_low_stock_alert.short_description = "Set low stock alert for selected products"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category', 'created_by')


# Enhanced UserProfile Admin
class EnhancedUserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'image_preview', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username', 'user__email', 'phone_number', 'address')
    readonly_fields = ('image_preview', 'created_at', 'updated_at')
    list_per_page = 50
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Contact Information', {
            'fields': ('phone_number', 'address')
        }),
        ('Personal Information', {
            'fields': ('date_of_birth',)
        }),
        ('Profile Picture', {
            'fields': ('profile_picture', 'image_preview')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.profile_picture:
            return format_html(
                '<img src="{}" style="width: 100px; height: 100px; object-fit: cover; border-radius: 50%; border: 2px solid #ddd;" />',
                obj.profile_picture.url
            )
        return format_html(
            '<div style="width: 100px; height: 100px; background: #f0f0f0; border-radius: 50%; display: flex; align-items: center; justify-content: center; border: 2px solid #ddd;">👤</div>'
        )
    image_preview.short_description = 'Profile Picture'


# Register models with enhanced admin classes
admin_site.register(User, EnhancedUserAdmin)
admin_site.register(Category, EnhancedCategoryAdmin)
admin_site.register(Product, EnhancedProductAdmin)
admin_site.register(UserProfile, EnhancedUserProfileAdmin)

