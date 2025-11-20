# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from appliances.models import ApplianceCategory, ApplianceProduct

class Command(BaseCommand):
    def handle(self, *args, **options):
        print('=== СТТСТ Ы ЫХ ===')
        
        categories_count = ApplianceCategory.objects.count()
        products_count = ApplianceProduct.objects.count()
        
        print(f'атегорий: {categories_count}')
        print(f'Товаров: {products_count}')
        
        # Статистика по категориям
        print('\nТоваров по категориям:')
        categories = ApplianceCategory.objects.all()
        for category in categories[:10]:  # окажем первые 10
            product_count = ApplianceProduct.objects.filter(category=category).count()
            print(f'- {category.name} ({category.code}): {product_count} товаров')
        
        print('\nоследние 5 товаров:')
        for product in ApplianceProduct.objects.all()[:5]:
            print(f'- {product.name}')
            print(f'  атегория: {product.category.name}')
            print(f'  роизводитель: {product.producer}')
            print(f'  ртикул: {product.part_number}')
            print('')
