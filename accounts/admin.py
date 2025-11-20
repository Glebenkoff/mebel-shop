from django.contrib import admin
from .models import LoyaltyProgram

@admin.register(LoyaltyProgram)
class LoyaltyProgramAdmin(admin.ModelAdmin):
    list_display = ['user', 'level', 'points', 'total_spent']
    list_filter = ['level']
    search_fields = ['user__username']
