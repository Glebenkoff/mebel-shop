# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from appliances.models import ApplianceCategory, ApplianceProduct
import json

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--action', type=str, default='stats', help='stats, categories, products, export-json')
        parser.add_argument('--limit', type=int, default=10, help='имит вывода')
        parser.add_argument('--category', type=str, help='ильтр по категории')
    
    def handle(self, *args, **options):
        action = options['action']
        
        if action == 'stats':
            self.show_stats()
        elif action == 'categories':
            self.show_categories(options['limit'])
        elif action == 'products':
            self.show_products(options['limit'], options['category'])
        elif action == 'export-json':
            self.export_json()
    
    def show_stats(self):
        self.stdout.write(self.style.SUCCESS('=== СТТСТ Ы ЫХ ==='))
        
        categories_count = ApplianceCategory.objects.count()
        products_count = ApplianceProduct.objects.count()
        products_without_price = ApplianceProduct.objects.filter(price__isnull=True).count()
        
        self.stdout.write(f'атегорий: {categories_count}')
        self.stdout.write(f'Товаров: {products_count}')
        self.stdout.write(f'Товаров без цены: {products_without_price}')
        
        # Топ категорий
        self.stdout.write('\nТоп категорий по количеству товаров:')
        categories = ApplianceCategory.objects.all()
        category_stats = []
        for category in categories:
            count = ApplianceProduct.objects.filter(category=category).count()
            if count > 0:
                category_stats.append((category.name, count))
        
        # Сортируем по убыванию количества товаров
        category_stats.sort(key=lambda x: x[1], reverse=True)
        
        for name, count in category_stats[:10]:
            self.stdout.write(f'  {name}: {count} товаров')
    
    def show_categories(self, limit):
        self.stdout.write(self.style.SUCCESS('=== СС Т ==='))
        
        categories = ApplianceCategory.objects.all()[:limit]
        for category in categories:
            product_count = ApplianceProduct.objects.filter(category=category).count()
            self.stdout.write(f'{category.code}: {category.name}')
            self.stdout.write(f'  Товаров: {product_count}')
            self.stdout.write('')
    
    def show_products(self, limit, category_filter):
        self.stdout.write(self.style.SUCCESS('=== СС Т ==='))
        
        products = ApplianceProduct.objects.all()
        
        if category_filter:
            products = products.filter(category__code=category_filter)
            self.stdout.write(f'ильтр: категория {category_filter}')
        
        products = products[:limit]
        
        for i, product in enumerate(products):
            self.stdout.write(f'{i+1}. {product.name}')
            self.stdout.write(f'   ID: {product.item_id}')
            self.stdout.write(f'   ртикул: {product.part_number}')
            self.stdout.write(f'   роизводитель: {product.producer}')
            self.stdout.write(f'   атегория: {product.category.name}')
            self.stdout.write(f'   ена: {product.price or \"ет цены\"}')
            self.stdout.write(f'   аличие: {product.stock} шт.')
            self.stdout.write('')
    
    def export_json(self):
        self.stdout.write(self.style.SUCCESS('=== СТ  JSON ==='))
        
        data = {
            'stats': {
                'categories_count': ApplianceCategory.objects.count(),
                'products_count': ApplianceProduct.objects.count(),
            },
            'categories': [],
            'products_sample': []
        }
        
        # кспортируем категории
        for category in ApplianceCategory.objects.all()[:20]:
            data['categories'].append({
                'code': category.code,
                'name': category.name,
                'product_count': ApplianceProduct.objects.filter(category=category).count()
            })
        
        # кспортируем пример товаров
        for product in ApplianceProduct.objects.all()[:10]:
            data['products_sample'].append({
                'item_id': product.item_id,
                'name': product.name,
                'part_number': product.part_number,
                'producer': product.producer,
                'category': product.category.name,
                'price': str(product.price) if product.price else None,
                'stock': product.stock
            })
        
        # Сохраняем в файл
        import os
        from django.conf import settings
        
        export_dir = os.path.join(settings.BASE_DIR, 'exports')
        os.makedirs(export_dir, exist_ok=True)
        
        json_file = os.path.join(export_dir, 'appliances_data.json')
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        self.stdout.write(f'анные экспортированы в: {json_file}')
