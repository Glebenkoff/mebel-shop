# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
import requests
import json

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--product-id', type=str, help='ID товара')
    
    def handle(self, *args, **options):
        product_id = options.get('product_id') or '2000045963'  # ример ID
        
        print('=== С ENDPOINT Я  ===')
        
        OCS_URL = 'https://testconnector.b2b.ocs.ru'
        TOKEN = 'n*WpKPp-WYB5edu8P-XrDmjeyuht1K'
        
        headers = {
            'X-API-Key': TOKEN,
            'Content-Type': 'application/json'
        }
        
        # робуем разные endpoints для получения цен
        endpoints = [
            f'/api/v2/prices/{product_id}',
            f'/api/v2/products/{product_id}/prices',
            f'/api/v2/catalog/products/{product_id}/prices',
            f'/api/v2/price/{product_id}',
        ]
        
        for endpoint in endpoints:
            print(f'\nробуем: {endpoint}')
            try:
                response = requests.get(OCS_URL + endpoint, headers=headers)
                print(f'Статус: {response.status_code}')
                
                if response.status_code == 200:
                    data = response.json()
                    print('спех! анные:')
                    print(json.dumps(data, ensure_ascii=False, indent=2)[:500])
                    break
                else:
                    print(f'Текст ответа: {response.text[:200]}')
                    
            except Exception as e:
                print(f'шибка: {e}')
