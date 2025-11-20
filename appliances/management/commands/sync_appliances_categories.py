from django.core.management.base import BaseCommand
from django.utils.text import slugify
import requests
import json

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('=== СХЯ Т ТХ ===')
        
        OCS_URL = 'https://testconnector.b2b.ocs.ru'
        TOKEN = 'n*WpKPp-WYB5edu8P-XrDmjeyuht1K'
        
        headers = {
            'X-API-Key': TOKEN,
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.get(f'{OCS_URL}/api/v2/catalog/categories', headers=headers)
            
            if response.status_code == 200:
                categories_data = response.json()
                self.stdout.write(self.style.SUCCESS(f'олучено категорий: {len(categories_data)}'))
                
                # щем категорию техники V07
                tech_category = self.find_technology_category(categories_data)
                if tech_category:
                    category_name = tech_category.get('name', 'Unknown')
                    self.stdout.write(self.style.SUCCESS(f'айдена категория техники: {category_name}'))
                    self.print_category_structure(tech_category)
                else:
                    self.stdout.write(self.style.ERROR('атегория техники V07 не найдена'))
                    
            else:
                self.stdout.write(self.style.ERROR(f'шибка API: {response.status_code}'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'шибка: {e}'))
    
    def find_technology_category(self, categories_data):
        # щем категорию V07 - ытовая техника и электроника
        for category in categories_data:
            if category.get('category') == 'V07':
                return category
        return None
    
    def print_category_structure(self, category, level=0):
        indent = '  ' * level
        category_code = category.get('category', '')
        category_name = category.get('name', '')
        
        self.stdout.write(f'{indent}{category_code}: {category_name}')
        
        # брабатываем дочерние категории
        children = category.get('children', [])
        for child in children:
            self.print_category_structure(child, level + 1)
