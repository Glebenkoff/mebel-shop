# appliances/management/commands/sync_appliances_products.py
@"
from django.core.management.base import BaseCommand
from appliances.models import ApplianceCategory, ApplianceProduct
import requests
from decimal import Decimal

class Command(BaseCommand):
    help = 'Синхронизация товаров техники с OCS'
    
    def add_arguments(self, parser):
        parser.add_argument('--category', type=str, help='Код категории для синхронизации')
        parser.add_argument('--limit', type=int, default=50, help='Лимит товаров')
    
    def handle(self, *args, **options):
        self.stdout.write('=== СИНХРОНИЗАЦИЯ ТОВАРОВ ТЕХНИКИ ===')
        
        category_code = options['category']
        limit = options['limit']
        
        if category_code:
            # Синхронизируем конкретную категорию
            categories = ApplianceCategory.objects.filter(ocs_category_code=category_code)
        else:
            # Синхронизируем все категории
            categories = ApplianceCategory.objects.all()
        
        for category in categories:
            self.stdout.write(f'Синхронизация категории: {category.name}')
            self._sync_products_for_category(category, limit)
    
    def _sync_products_for_category(self, category, limit):
        \"\"\"Синхронизация товаров для категории\"\"\"
        OCS_URL = 'https://testconnector.b2b.ocs.ru'
        TOKEN = 'n*WpKPp-WYB5edu8P-XrDmjeyuht1K'
        
        headers = {
            'Authorization': f'Bearer {TOKEN}',
            'Content-Type': 'application/json'
        }
        
        try:
            # Получаем товары категории
            response = requests.get(
                f'{OCS_URL}/api/v2/catalog/categories/{category.ocs_category_code}/products',
                headers=headers
            )
            
            if response.status_code == 200:
                products_data = response.json()
                self._process_products(products_data[:limit], category)
            else:
                self.stdout.write(self.style.ERROR(f'Ошибка для категории {category.name}: {response.status_code}'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка: {e}'))
    
    def _process_products(self, products_data, category):
        \"\"\"Обработка и сохранение товаров\"\"\"
        for product_data in products_data:
            product_code = product_data.get('itemId')
            
            if not product_code:
                continue
            
            # Создаем или обновляем товар
            product, created = ApplianceProduct.objects.get_or_create(
                ocs_product_code=product_code,
                defaults={
                    'name': product_data.get('name', ''),
                    'description': product_data.get('description', ''),
                    'category': category,
                    'price': Decimal(product_data.get('price', 0)),
                    'brand': product_data.get('brand', ''),
                    'characteristics': product_data.get('characteristics', {}),
                    'stock_quantity': product_data.get('stock', 0),
                    'in_stock': product_data.get('stock', 0) > 0
                }
            )
            
            status = 'СОЗДАН' if created else 'ОБНОВЛЕН'
            self.stdout.write(f'{status}: {product.name}')
"@ | Out-File appliances\management\commands\sync_appliances_products.py -Encoding utf8