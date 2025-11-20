# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from appliances.models import ApplianceProduct
import csv
import os
from django.conf import settings

class Command(BaseCommand):
    def handle(self, *args, **options):
        print('=== СТ Т  CSV ===')
        
        # Создаем папку для экспорта если не существует
        export_dir = os.path.join(settings.BASE_DIR, 'exports')
        os.makedirs(export_dir, exist_ok=True)
        
        csv_file = os.path.join(export_dir, 'appliances_export.csv')
        
        products = ApplianceProduct.objects.all()
        
        with open(csv_file, 'w', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file, delimiter=';')
            
            # аголовки
            writer.writerow([
                'ID', 'азвание', 'усское название', 'ртикул', 
                'роизводитель', 'ренд', 'атегория', 'аличие', 'ена'
            ])
            
            # анные
            for product in products:
                writer.writerow([
                    product.item_id,
                    product.name,
                    product.russian_name,
                    product.part_number,
                    product.producer,
                    product.brand,
                    product.category.name,
                    product.stock,
                    product.price or 'ет цены'
                ])
        
        print(f'кспортировано товаров: {products.count()}')
        print(f'айл: {csv_file}')
