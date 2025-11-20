from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from catalog.models import PartnerProduct

#class Cart(models.Model):
#    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
#    session_id = models.CharField(max_length=100, null=True, blank=True)
#    created_at = models.DateTimeField(auto_now_add=True)

#    def __str__(self):
#        return f"Cart {self.id} — {self.user or self.session_id}"

#class CartItem(models.Model):
#    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
#    product = models.ForeignKey(PartnerProduct, on_delete=models.CASCADE)
#    quantity = models.PositiveIntegerField(default=1)
#
#    def __str__(self):
#        return f"{self.quantity} x {self.product.name}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=20, unique=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    shipping_address = models.TextField()
    billing_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Order {self.order_number}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.quantity} x {self.product_name}'