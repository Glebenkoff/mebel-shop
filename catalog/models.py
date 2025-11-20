from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ('name',)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    
    class Meta:
        ordering = ('name',)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('product_detail', args=[self.id])

class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name='wishlists')
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Wishlist of {self.user.username}'

class Comparison(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name='comparisons')
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Comparison of {self.user.username}'
    
    def can_add_more(self):
        return self.products.count() < 4
