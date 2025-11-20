# -*- coding: utf-8 -*-
from django.contrib import admin
from appliances.models import ApplianceCategory, ApplianceProduct

@admin.register(ApplianceCategory)
class ApplianceCategoryAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'parent', 'created_at']
    list_filter = ['created_at']
    search_fields = ['code', 'name']
    ordering = ['code']

@admin.register(ApplianceProduct)
class ApplianceProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'producer', 'price', 'stock', 'sync_date']
    list_filter = ['category', 'producer', 'sync_date']
    search_fields = ['name', 'russian_name', 'part_number', 'item_id']
    readonly_fields = ['sync_date']
    ordering = ['-sync_date']
    
    fieldsets = (
        ('сновная информация', {
            'fields': ('item_id', 'name', 'russian_name', 'product_name', 'description')
        }),
        ('лассификация', {
            'fields': ('category', 'producer', 'brand', 'part_number')
        }),
        ('ены и наличие', {
            'fields': ('price', 'stock', 'warranty', 'condition')
        }),
        ('ополнительно', {
            'fields': ('line_code', 'ean128', 'vat_percent', 'is_active', 'sync_date')
        }),
    )
