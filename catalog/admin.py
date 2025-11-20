from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)  
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'available']
    list_filter = ['available', 'category']
    prepopulated_fields = {'slug': ('name',)}
