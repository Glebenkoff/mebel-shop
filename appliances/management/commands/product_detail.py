from django.core.management.base import BaseCommand
import requests
import json

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--category', type=str, required=True, help='од категории')
        parser.add_argument('--product-index', type=int, default=0, help='ндекс товара в списке')
    
    def handle(self, *args, **options):
        category_code = options['category']
        product_index = options['product_index']
        
        print('=== ТЬЯ Я  Т ===')
        print('атегория: ' + category_code)
        print('ндекс товара: ' + str(product_index))
        
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
                    
                    if product_index < len(products_list):
                        product_item = products_list[product_index]
                        product_data = product_item.get('product', {})
                        
                        print('Товар: ' + product_data.get('name', 'No name'))
                        print('')
                        print('СЯ Я:')
                        print('  ID: ' + str(product_data.get('itemId', 'N/A')))
                        print('  ртикул: ' + str(product_data.get('partNumber', 'N/A')))
                        print('  ена: ' + str(product_data.get('price', 'N/A')))
                        print('  ренд: ' + str(product_data.get('brand', 'N/A')))
                        print('  аличие: ' + str(product_data.get('stock', 0)) + ' шт.')
                        print('  атегория: ' + str(product_data.get('category', 'N/A')))
                        print('')
                        print('С Я Т:')
                        for key, value in product_data.items():
                            print('  ' + key + ': ' + str(value))
                    else:
                        print('Товар с индексом ' + str(product_index) + ' не найден')
                        print('сего товаров: ' + str(len(products_list)))
                        
                else:
                    print('еожиданный формат данных')
                    
            else:
                print('шибка API: ' + str(response.status_code))
                
        except Exception as e:
            print('шибка: ' + str(e))
