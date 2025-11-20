# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from appliances.models import ApplianceProduct

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--limit', type=int, default=5, help='имит товаров')
    
    def handle(self, *args, **options):
        limit = options['limit']
        
        print('=== Т Т  Ы ===')
        
        products = ApplianceProduct.objects.all()[:limit]
        
        for i, product in enumerate(products):
            print(f'\n{i+1}. {product.name}')
            print(f'   ID: {product.item_id}')
            print(f'   ртикул: {product.part_number}')
            print(f'   роизводитель: {product.producer}')
            print(f'   ренд: {product.brand}')
            print(f'   атегория: {product.category.name}')
            print(f'   аличие: {product.stock} шт.')
            print(f'   ена: {product.price}')
            print(f'   арантия: {product.warranty}')
            
            if product.description:
                print(f'   писание: {product.description[:100]}...')
