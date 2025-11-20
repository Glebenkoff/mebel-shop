from django.core.management.base import BaseCommand
import requests
import json

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('=== Я СХЯ ТХ ===')
        
        OCS_URL = 'https://testconnector.b2b.ocs.ru'
        TOKEN = 'n*WpKPp-WYB5edu8P-XrDmjeyuht1K'
        
        headers = {
            'X-API-Key': TOKEN,
            'Content-Type': 'application/json'
        }
        
        # 1. олучаем все категории
        self.stdout.write('1. олучаем категории...')
        response = requests.get(f'{OCS_URL}/api/v2/catalog/categories', headers=headers)
        
        if response.status_code != 200:
            self.stdout.write(self.style.ERROR('шибка получения категорий'))
            return
        
        categories_data = response.json()
        tech_categories = self.extract_technology_categories(categories_data)
        
        self.stdout.write(self.style.SUCCESS(f'айдено категорий техники: {len(tech_categories)}'))
        
        # 2. олучаем товары из каждой категории техники
        total_products = 0
        for category in tech_categories[:3]:  # граничимся 3 категориями для теста
            category_code = category.get('category', '')
            category_name = category.get('name', '')
            
            self.stdout.write(f'\n2. атегория: {category_name} ({category_code})')
            
            products_response = requests.get(
                f'{OCS_URL}/api/v2/catalog/categories/{category_code}/products', 
                headers=headers
            )
            
            if products_response.status_code == 200:
                products_data = products_response.json()
                
                # роверяем формат ответа
                if isinstance(products_data, list):
                    products_count = len(products_data)
                    self.stdout.write(f'   Товаров: {products_count}')
                    total_products += products_count
                    
                    # окажем несколько товаров
                    for product in products_data[:2]:
                        product_name = product.get('name', 'No name')
                        product_price = product.get('price', 'N/A')
                        self.stdout.write(f'   - {product_name} - {product_price} руб.')
                else:
                    # сли это не список, возможно это словарь с другой структурой
                    self.stdout.write(f'   ормат данных: {type(products_data)}')
                    self.stdout.write(f'   лючи: {list(products_data.keys())}')
                    
            else:
                self.stdout.write(f'   ет товаров: {products_response.status_code}')
        
        self.stdout.write(self.style.SUCCESS(f'\nсего товаров техники: {total_products}'))
    
    def extract_technology_categories(self, categories_data):
        # звлекаем все категории из V07 (ытовая техника)
        tech_categories = []
        
        for category in categories_data:
            if category.get('category') == 'V07':
                # обавляем саму категорию V07 и все её подкатегории
                tech_categories.append(category)
                tech_categories.extend(self.get_all_subcategories(category))
        
        return tech_categories
    
    def get_all_subcategories(self, category):
        # екурсивно получаем все подкатегории
        subcategories = []
        children = category.get('children', [])
        
        for child in children:
            subcategories.append(child)
            subcategories.extend(self.get_all_subcategories(child))
        
        return subcategories
