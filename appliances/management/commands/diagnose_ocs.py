from django.core.management.base import BaseCommand
import requests

class Command(BaseCommand):
    def handle(self, *args, **options):
        print('=== СТ OCS API ===')
        
        OCS_URL = 'https://testconnector.b2b.ocs.ru'
        TOKEN = 'n*WpKPp-WYB5edu8P-XrDmjeyuht1K'
        
        print(f'URL: {OCS_URL}')
        print(f'Token: {TOKEN[:10]}...')
        
        # Тест 1: роверка сервера
        print('\n1. роверка сервера...')
        try:
            response = requests.get(OCS_URL, timeout=10)
            print(f'   Сервер доступен: {response.status_code}')
        except Exception as e:
            print(f'   Сервер недоступен: {e}')
            return
        
        # Тест 2: окументация
        print('\n2. роверка документации...')
        try:
            response = requests.get(f'{OCS_URL}/docs/index.html', timeout=10)
            print(f'   окументация: {response.status_code}')
        except Exception as e:
            print(f'   окументация: {e}')
        
        # Тест 3: орматы авторизации
        print('\n3. Тестируем авторизацию:')
        
        methods = [
            {'name': 'Bearer', 'headers': {'Authorization': f'Bearer {TOKEN}'}},
            {'name': 'API Key', 'headers': {'X-API-Key': TOKEN}},
        ]
        
        for method in methods:
            print(f'\n   {method["name"]}:')
            headers = method['headers']
            headers['Content-Type'] = 'application/json'
            
            try:
                response = requests.get(f'{OCS_URL}/api/v2/catalog/categories', headers=headers, timeout=10)
                print(f'      Статус: {response.status_code}')
                
                if response.status_code == 200:
                    print('      ✅ СХ!')
                    data = response.json()
                    print(f'      атегорий: {len(data)}')
                    if data:
                        sample = data[0]
                        print(f'      ример: {sample.get("category")} - {sample.get("name")}')
                    return
                    
            except Exception as e:
                print(f'      шибка: {e}')
        
        print('\n===  ===')
        print('1. роверьте токен в панели OCS')
        print('2. бедитесь что IP разрешен')
        print('3. роверьте документацию OCS')
        print('4. Свяжитесь с поддержкой OCS')
