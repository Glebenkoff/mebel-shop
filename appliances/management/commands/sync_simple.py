from django.core.management.base import BaseCommand
import requests

class Command(BaseCommand):
    def handle(self, *args, **options):
        print('=== СХЯ ТХ ===')
        
        OCS_URL = 'https://testconnector.b2b.ocs.ru'
        TOKEN = 'n*WpKPp-WYB5edu8P-XrDmjeyuht1K'
        
        headers = {
            'X-API-Key': TOKEN,
            'Content-Type': 'application/json'
        }
        
        # олучаем категории
        print('1. олучаем категории...')
        response = requests.get(OCS_URL + '/api/v2/catalog/categories', headers=headers)
        
        if response.status_code != 200:
            print('шибка получения категорий')
            return
        
        categories_data = response.json()
        
        # щем категорию техники V07
        tech_categories = []
        for category in categories_data:
            if category.get('category') == 'V07':
                tech_categories = self.get_all_subcategories(category)
                break
        
        print('айдено категорий техники: ' + str(len(tech_categories)))
        
        # олучаем товары из первых 3 категорий
        total_products = 0
        for category in tech_categories[:3]:
            category_code = category.get('category', '')
            category_name = category.get('name', '')
            
            print('2. атегория: ' + category_name + ' (' + category_code + ')')
            
            products_response = requests.get(
                OCS_URL + '/api/v2/catalog/categories/' + category_code + '/products', 
                headers=headers
            )
            
            if products_response.status_code == 200:
                data = products_response.json()
                
                if isinstance(data, dict) and 'result' in data:
                    products_list = data['result']
                    products_count = len(products_list)
                    print('   Товаров: ' + str(products_count))
                    total_products += products_count
                    
                    # окажем первые 2 товара
                    for product_item in products_list[:2]:
                        product_data = product_item.get('product', {})
                        product_name = product_data.get('name', 'No name')
                        product_price = product_data.get('price', 'N/A')
                        print('   - ' + product_name + ' - ' + str(product_price) + ' руб.')
                else:
                    print('   ормат данных не распознан')
            else:
                print('   шибка: ' + str(products_response.status_code))
        
        print('сего товаров техники: ' + str(total_products))
    
    def get_all_subcategories(self, category):
        subcategories = []
        children = category.get('children', [])
        
        for child in children:
            subcategories.append(child)
            subcategories.extend(self.get_all_subcategories(child))
        
        return subcategories
