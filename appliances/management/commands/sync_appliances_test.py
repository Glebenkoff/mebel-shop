from django.core.management.base import BaseCommand
import requests
import json

class Command(BaseCommand):
    help = 'Тестовая синхронизация техники'
    
    def add_arguments(self, parser):
        parser.add_argument('--limit', type=int, default=5, help='Лимит категорий для показа')
    
    def handle(self, *args, **options):
        self.stdout.write('=== ТЕСТ СИНХРОНИЗАЦИИ ТЕХНИКИ ===')
        
        OCS_URL = 'https://testconnector.b2b.ocs.ru'
        TOKEN = 'n*WpKPp-WYB5edu8P-XrDmjeyuht1K'
        
        headers = {
            'Authorization': f'Bearer {TOKEN}',
            'Content-Type': 'application/json'
        }
        
        try:
            # 1. Получаем категории
            self.stdout.write('1. Получаем категории...')
            response = requests.get(f'{OCS_URL}/api/v2/catalog/categories', headers=headers)
            
            if response.status_code == 200:
                categories = response.json()
                self.stdout.write(self.style.SUCCESS(f'Получено категорий: {len(categories)}'))
                
                # Ищем категорию техники V07
                tech_categories = self.find_technology_categories(categories)
                self.stdout.write(f'Найдено категорий техники: {len(tech_categories)}')
                
                # 2. Показываем несколько товаров из первой категории техники
                if tech_categories:
                    self.show_sample_products(tech_categories[0], OCS_URL, headers, options['limit'])
                    
            else:
                self.stdout.write(self.style.ERROR(f'Ошибка API: {response.status_code}'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка: {e}'))
    
    def find_technology_categories(self, categories_data):
        # Поиск категорий техники
        tech_categories = []
        
        for category in categories_data:
            if category.get('category') == 'V07':
                tech_categories.append(category)
                # Также добавляем все дочерние категории
                tech_categories.extend(self.get_all_subcategories(category))
        
        return tech_categories
    
    def get_all_subcategories(self, category):
        # Получение всех подкатегорий
        subcategories = []
        children = category.get('children', [])
        
        for child in children:
            subcategories.append(child)
            subcategories.extend(self.get_all_subcategories(child))
        
        return subcategories
    
    def show_sample_products(self, category, ocs_url, headers, limit):
        # Показ примеров товаров из категории
        category_code = category.get('category')
        category_name = category.get('name')
        
        self.stdout.write(f'2. Товары из категории: {category_name} ({category_code})')
        
        try:
            response = requests.get(
                f'{ocs_url}/api/v2/catalog/categories/{category_code}/products', 
                headers=headers
            )
            
            if response.status_code == 200:
                products = response.json()
                self.stdout.write(self.style.SUCCESS(f'Получено товаров: {len(products)}'))
                
                # Показываем первые N товаров
                for i, product in enumerate(products[:limit]):
                    self.stdout.write(f'   {i+1}. {product.get(\"name\", \"No name\")}')
                    self.stdout.write(f'      Цена: {product.get(\"price\", \"N/A\")}')
                    self.stdout.write(f'      Бренд: {product.get(\"brand\", \"N/A\")}')
                    
            else:
                self.stdout.write(self.style.WARNING(f'Нет товаров или ошибка: {response.status_code}'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка получения товаров: {e}'))
