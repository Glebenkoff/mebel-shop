from django.core.management.base import BaseCommand
import requests
import json

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--category', type=str, default='V070000', help='од категории')
        parser.add_argument('--limit', type=int, default=10, help='имит товаров')
    
    def handle(self, *args, **options):
        category_code = options['category']
        limit = options['limit']
        
        self.stdout.write(f'=== ТЫ  Т {category_code} ===')
        
        OCS_URL = 'https://testconnector.b2b.ocs.ru'
        TOKEN = 'n*WpKPp-WYB5edu8P-XrDmjeyuht1K'
        
        headers = {
            'X-API-Key': TOKEN,
            'Content-Type': 'application/json'
        }
        
        try:
            # олучаем товары категории
            response = requests.get(
                f'{OCS_URL}/api/v2/catalog/categories/{category_code}/products', 
                headers=headers
            )
            
            if response.status_code == 200:
                products_data = response.json()
                self.stdout.write(self.style.SUCCESS(f'олучено товаров: {len(products_data)}'))
                
                # оказываем товары
                for i, product in enumerate(products_data[:limit]):
                    product_name = product.get('name', 'No name')
                    product_id = product.get('itemId', 'N/A')
                    product_price = product.get('price', 'N/A')
                    product_brand = product.get('brand', 'N/A')
                    product_stock = product.get('stock', 0)
                    
                    self.stdout.write(f'\n{i+1}. {product_name}')
                    self.stdout.write(f'   ID: {product_id}')
                    self.stdout.write(f'   ена: {product_price}')
                    self.stdout.write(f'   ренд: {product_brand}')
                    self.stdout.write(f'   аличие: {product_stock} шт.')
                    
            else:
                self.stdout.write(self.style.ERROR(f'шибка: {response.status_code} - {response.text}'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'шибка: {e}'))
