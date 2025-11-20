from django.contrib import admin
from .models import Order, OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_number', 'user', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['order_number', 'user__username']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product_name', 'quantity', 'product_price', 'total_price']
    list_filter = ['order__status']