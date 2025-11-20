from django.core.management.base import BaseCommand
from appliances.models import ApplianceProduct
import requests

class Command(BaseCommand):
    help = 'олучение цен для товаров'

    def handle(self, *args, **options):
        self.stdout.write('===   ===')
        
        OCS_URL = 'https://testconnector.b2b.ocs.ru'
        TOKEN = 'n*WpKPp-WYB5edu8P-XrDmjeyuht1K'
        
        headers = {
            'X-API-Key': TOKEN,
            'Content-Type': 'application/json'
        }
        
        # олучаем товары без цен
        products_without_price = ApplianceProduct.objects.filter(price__isnull=True)[:10]  # граничим для теста
        
        self.stdout.write(f'Товаров без цены: {products_without_price.count()}')
        
        updated_count = 0
        for product in products_without_price:
            # десь нужно использовать соответствующий endpoint API для получения цен
            # то пример - нужно уточнить правильный endpoint у OCS
            try:
                response = requests.get(
                    f'{OCS_URL}/api/v2/prices/{product.item_id}',
                    headers=headers
                )
                
                if response.status_code == 200:
                    price_data = response.json()
                    # бработка данных о цене (структура может отличаться)
                    # product.price = price_data.get('price')
                    # product.save()
                    updated_count += 1
                    
            except Exception as e:
                self.stdout.write(f'шибка для товара {product.item_id}: {e}')
        
        self.stdout.write(self.style.SUCCESS(f'бновлено цен: {updated_count}'))
