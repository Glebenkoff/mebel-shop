# appliances/management/commands/sync_appliances_stock_prices.py
@"
from django.core.management.base import BaseCommand
from appliances.models import ApplianceProduct
import requests
from decimal import Decimal
from django.utils import timezone

class Command(BaseCommand):
    help = 'Быстрая синхронизация наличия и цен'
    
    def handle(self, *args, **options):
        self.stdout.write('=== СИНХРОНИЗАЦИЯ НАЛИЧИЯ И ЦЕН ===')
        
        OCS_URL = 'https://testconnector.b2b.ocs.ru'
        TOKEN = 'n*WpKPp-WYB5edu8P-XrDmjeyuht1K'
        
        # Получаем товары которые нужно обновить
        products = ApplianceProduct.objects.filter(is_active=True)
        product_codes = [p.ocs_product_code for p in products]
        
        if not product_codes:
            self.stdout.write('Нет товаров для обновления')
            return
        
        # Разбиваем на батчи по 50 товаров (ограничение API)
        batch_size = 50
        updated_count = 0
        
        for i in range(0, len(product_codes), batch_size):
            batch = product_codes[i:i + batch_size]
            self._update_batch(batch, OCS_URL, TOKEN)
            updated_count += len(batch)
        
        self.stdout.write(self.style.SUCCESS(f'Обновлено товаров: {updated_count}'))
    
    def _update_batch(self, product_codes, ocs_url, token):
        \"\"\"Обновление батча товаров\"\"\"
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        try:
            # Используем batch endpoint для массового обновления
            response = requests.post(
                f'{ocs_url}/api/v2/catalog/products/batch',
                headers=headers,
                json=product_codes
            )
            
            if response.status_code == 200:
                products_data = response.json()
                self._process_stock_updates(products_data)
            else:
                self.stdout.write(self.style.ERROR(f'Ошибка batch запроса: {response.status_code}'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка: {e}'))
    
    def _process_stock_updates(self, products_data):
        \"\"\"Обработка обновлений наличия и цен\"\"\"
        for product_data in products_data:
            product_code = product_data.get('itemId')
            
            if not product_code:
                continue
            
            try:
                product = ApplianceProduct.objects.get(ocs_product_code=product_code)
                product.price = Decimal(product_data.get('price', product.price))
                product.stock_quantity = product_data.get('stock', product.stock_quantity)
                product.in_stock = product_data.get('stock', 0) > 0
                product.last_sync_date = timezone.now()
                product.save()
                
                self.stdout.write(f'✓ {product.name}: {product.price} руб., {product.stock_quantity} шт.')
                
            except ApplianceProduct.DoesNotExist:
                self.stdout.write(f'⚠ Товар не найден: {product_code}')
"@ | Out-File appliances\management\commands\sync_appliances_stock_prices.py -Encoding utf8