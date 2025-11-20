from django.core.management.base import BaseCommand
import requests
import json

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--category', type=str, default='V070000', help='од категории')
    
    def handle(self, *args, **options):
        category_code = options['category']
        
        print('=== Т Т ЫХ ===')
        print('атегория: ' + category_code)
        
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
            
            print('Статус: ' + str(response.status_code))
            
            if response.status_code == 200:
                data = response.json()
                
                print('Тип данных: ' + str(type(data)))
                
                if isinstance(data, list):
                    print('ормат: Список')
                    print('оличество элементов: ' + str(len(data)))
                    if data:
                        print('ервый элемент:')
                        print(json.dumps(data[0], ensure_ascii=False, indent=2))
                elif isinstance(data, dict):
                    print('ормат: Словарь')
                    print('лючи: ' + str(list(data.keys())))
                    # окажем первые 3 ключа
                    for key, value in list(data.items())[:3]:
                        print('  ' + key + ': ' + str(type(value)) + ' - ' + str(value)[:100])
                else:
                    print('еизвестный формат')
                    print(str(data)[:500])
                    
            else:
                print('шибка: ' + str(response.status_code))
                print('Текст: ' + response.text[:200])
                
        except Exception as e:
            print('шибка: ' + str(e))
