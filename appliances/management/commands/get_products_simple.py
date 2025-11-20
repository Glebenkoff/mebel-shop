from django.core.management.base import BaseCommand
import requests

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--category', type=str, required=True, help='од категории')
        parser.add_argument('--limit', type=int, default=5, help='имит товаров')
    
    def handle(self, *args, **options):
        category_code = options['category']
        limit = options['limit']
        
        print('=== ТЫ Т ' + category_code + ' ===')
        
        OCS_URL = 'https://testconnector.b2b.ocs.ru'
        TOKEN = 'n*WpKPp-WYB5edu8P-XrDmjeyuht1K'
        
        headers = {
            'X-API-Key': TOKEN,
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.get(
                OCS_URL + '/api/v2/catalog/categories/' + category_code + '/products', 
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if isinstance(data, dict) and 'result' in data:
                    products_list = data['result']
                    print('айдено товаров: ' + str(len(products_list)))
                    
                    for i, product_item in enumerate(products_list[:limit]):
                        product_data = product_item.get('product', {})
                        print(str(i+1) + '. ' + product_data.get('name', 'No name'))
                        print('   ID: ' + str(product_data.get('itemId', 'N/A')))
                        print('   ртикул: ' + str(product_data.get('partNumber', 'N/A')))
                        print('   ена: ' + str(product_data.get('price', 'N/A')))
                        print('   ренд: ' + str(product_data.get('brand', 'N/A')))
                        print('   аличие: ' + str(product_data.get('stock', 0)) + ' шт.')
                        print('')
                        
                else:
                    print('еожиданный формат данных')
                    print('лючи: ' + str(list(data.keys())))
                    
            else:
                print('шибка API: ' + str(response.status_code))
                print('твет: ' + response.text[:200])
                
        except Exception as e:
            print('шибка: ' + str(e))
