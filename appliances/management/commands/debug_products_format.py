from django.core.management.base import BaseCommand
import requests
import json

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--category', type=str, default='V070000', help='од категории')
    
    def handle(self, *args, **options):
        category_code = options['category']
        
        self.stdout.write(f'=== Т Т ЫХ Я {category_code} ===')
        
        OCS_URL = 'https://testconnector.b2b.ocs.ru'
        TOKEN = 'n*WpKPp-WYB5edu8P-XrDmjeyuht1K'
        
        headers = {
            'X-API-Key': TOKEN,
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.get(
                f'{OCS_URL}/api/v2/catalog/categories/{category_code}/products', 
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                
                self.stdout.write(f'Тип данных: {type(data)}')
                self.stdout.write(f'лина данных: {len(data) if isinstance(data, (list, dict)) else \"N/A\"}')
                
                if isinstance(data, list):
                    self.stdout.write('ормат: Список товаров')
                    if data:
                        self.stdout.write('ервый товар:')
                        self.print_product_info(data[0])
                elif isinstance(data, dict):
                    self.stdout.write('ормат: Словарь')
                    self.stdout.write(f'лючи: {list(data.keys())}')
                    # окажем структуру
                    for key, value in list(data.items())[:3]:
                        self.stdout.write(f'  {key}: {type(value)} - {str(value)[:100]}...')
                else:
                    self.stdout.write(f'еизвестный формат: {data}')
                    
            else:
                self.stdout.write(self.style.ERROR(f'шибка: {response.status_code}'))
                self.stdout.write(f'Текст ответа: {response.text}')
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'шибка: {e}'))
    
    def print_product_info(self, product):
        if isinstance(product, dict):
            for key, value in product.items():
                self.stdout.write(f'    {key}: {value}')
        else:
            self.stdout.write(f'    {product}')
