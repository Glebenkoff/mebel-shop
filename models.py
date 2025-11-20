from django.db import models
from catalog.models import Product

class Cart(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Cart {self.id}'
    
    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())
    
    def get_items_count(self):
        return sum(item.quantity for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    def __str__(self):
        return f'{self.quantity} x {self.product.name}'
    
    def get_total_price(self):
        return self.quantity * self.product.price
