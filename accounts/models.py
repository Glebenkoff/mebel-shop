from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

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
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    email_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f"Profile: {self.user.username}"

# Сигналы для автоматического создания профилей
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profiles(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        LoyaltyProgram.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()