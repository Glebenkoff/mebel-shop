from django.db import models
from catalog.models import Product
from django.contrib.auth.models import User
from django.conf import settings

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Cart {self.id} (User: {self.user.username})'  # ОБНОВИТЬ

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())

    def get_total_quantity(self):  # ПЕРЕИМЕНОВАТЬ get_items_count
        return sum(item.quantity for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    def __str__(self):
        return f'{self.quantity} x {self.product.name}'
    
    def get_total_price(self):
        return self.quantity * self.product.price
    
#class Review(models.Model):
#    product = models.ForeignKey(Product, on_delete=models.CASCADE)
#    user = models.ForeignKey(User, on_delete=models.CASCADE)
#    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
#    text = models.TextField(max_length=1000)
#    created_at = models.DateTimeField(auto_now_add=True)
#    is_approved = models.BooleanField(default=True)

    def __str__(self):
        return f"Отзыв {self.user} на {self.product}"
