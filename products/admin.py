from django.contrib import admin
from django.utils.html import format_html
from .models import Product

# Constants
NO_IMAGE_TEXT = "No Image"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock_status', 'stock_quantity', 
                   'is_active', 'image_preview', 'created_at')
    list_filter = ('category', 'is_active', 'created_at', 'updated_at', 'created_by')
    search_fields = ('name', 'description', 'category__name', 'created_by__username')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at', 'image_preview', 'stock_status')
    list_editable = ('is_active', 'stock_quantity')
    list_per_page = 25
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
    
    def stock_status(self, obj):
        status = obj.stock_status
        colors = {
            'Out of Stock': 'red',
            'In Stock': 'green'
        }
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            colors.get(status, 'black'),
            status
        )
    stock_status.short_description = 'Stock Status'
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 5px;" />',
                obj.image.url
            )
        return NO_IMAGE_TEXT
    image_preview.short_description = 'Image'
