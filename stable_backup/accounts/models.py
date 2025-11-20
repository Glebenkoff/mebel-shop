from django.db import models
from django.contrib.auth.models import User
#from django.conf import settings
#from django.contrib.auth.models import AbstractUser

class LoyaltyProgram(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    LEVELS = [
        ('bronze', '🥉 Бронза'),
        ('silver', '🥈 Серебро'), 
        ('gold', '🥇 Золото'),
        ('platinum', '💎 Платина'),
    ]
    
    points = models.PositiveIntegerField(default=0)
    level = models.CharField(max_length=20, choices=LEVELS, default='bronze')
    total_spent = models.DecimalField(max_digits=12, decimal_places=2, default=0)
        
    def __str__(self):
        return f"Loyalty: {self.user.username} ({self.level})"
    
    def add_points(self, amount):
        self.points += int(amount)
        self.update_level()
        self.save()
    
    def update_level(self):
        if self.total_spent >= 10000000:
            self.level = 'platinum'
        elif self.total_spent >= 5000000:
            self.level = 'gold'
        elif self.total_spent >= 2000000:
            self.level = 'silver'
        else:
            self.level = 'bronze'
    
    def get_discount_percent(self):
        discounts = {
            'bronze': 0,
            'silver': 5, 
            'gold': 10,
            'platinum': 15
        }
        return discounts.get(self.level, 0)

#class CustomUser(AbstractUser):
#    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
#    email_verified = models.BooleanField(default=False, verbose_name='Email подтвержден')
#    verification_token = models.CharField(max_length=100, blank=True)
#    
    # Добавляем related_name чтобы избежать конфликтов
#    groups = models.ManyToManyField(
#        'auth.Group',
#        verbose_name='groups',
#        blank=True,
#        help_text='The groups this user belongs to.',
#        related_name='customuser_set',  # Уникальное имя
#        related_query_name='customuser',
#    )
#    user_permissions = models.ManyToManyField(
#        'auth.Permission',
#        verbose_name='user permissions',
#        blank=True,
#        help_text='Specific permissions for this user.',
#        related_name='customuser_set',  # Уникальное имя
#        related_query_name='customuser',
#    )
#    
#    def __str__(self):
#        return f"{self.first_name} {self.last_name} ({self.email})"