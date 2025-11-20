from django.core.management.base import BaseCommand
from catalog.models import PartnerProduct, Category
from catalog.ocs_client import OCSClient
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Синхронизация товаров из OCS (исправленная версия)'

    def add_arguments(self, parser):
        parser.add_argument('--category', type=str, default='all', help='Код категории OCS')
        parser.add_argument('--limit', type=int, default=50, help='Лимит товаров')

    def handle(self, *args, **options):
        category_code = options['category']
        limit = options['limit']
        
        self.stdout.write(f'=== СИНХРОНИЗАЦИЯ ТОВАРОВ (категория: {category_code}) ===')
        
        client = OCSClient()
        
        # Получаем товары из OCS
        self.stdout.write(f'🔄 Получение товаров из OCS...')
        products_data = client.get_products_by_category(category_code)
        
        if not products_data:
            self.stdout.write('❌ Не удалось получить товары от OCS')
            return
        
        self.stdout.write(f'📦 Получено товаров от OCS: {len(products_data)}')
        
        created_count = 0
        updated_count = 0
        
        for i, product_item in enumerate(products_data[:limit]):
            try:
                # Обрабатываем структуру данных OCS v2
                product_data = product_item.get('product', {})
                price_data = product_item.get('price', {})
                
                # Извлекаем данные
                product_key = product_data.get('productKey')
                name = product_data.get('itemNameRus') or product_data.get('itemName', 'No name')
                producer = product_data.get('producer', '')
                ocs_item_id = product_data.get('itemId')
                
                # Цена
                price_value = price_data.get('value', 0)
                price = Decimal(str(price_value)) if price_value else Decimal('0')
                
                if not product_key:
                    self.stdout.write(f'⚠️ Пропущен товар без product_key: {name}')
                    continue
                
                # Находим категорию по имени производителя или другим признакам
                category = self._find_category_for_product(product_data, producer)
                
                # Проверяем существует ли товар
                product, created = PartnerProduct.objects.get_or_create(
                    product_key=product_key,
                    defaults={
                        'name': name,
                        'price': price,
                        'producer': producer,
                        'availability': product_item.get('isAvailableForOrder', False),
                        'ocs_item_id': ocs_item_id,
                        'part_number': product_data.get('partNumber', ''),
                        'original_price': price,
                        'currency': price_data.get('currency', 'RUR'),
                        'category': category,
                        'ocs_data': product_data  # Сохраняем полные данные
                    }
                )
                
                if created:
                    created_count += 1
                    self.stdout.write(f'✅ [{created_count}] Создан: {name}')
                    self.stdout.write(f'   💰 Цена: {price} ₽, Производитель: {producer}')
                else:
                    # Обновляем существующий товар
                    product.name = name
                    product.price = price
                    product.producer = producer
                    product.availability = product_item.get('isAvailableForOrder', False)
                    product.category = category
                    product.save()
                    updated_count += 1
                    self.stdout.write(f'🔄 Обновлен: {name}')
            
            except Exception as e:
                self.stdout.write(f'❌ Ошибка обработки товара: {e}')
                logger.error(f"Error processing product: {e}")
                continue
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n🎉 Синхронизация завершена! '
                f'Создано: {created_count}, Обновлено: {updated_count}'
            )
        )
        
        # Финальная статистика
        total_products = PartnerProduct.objects.count()
        self.stdout.write(f'📊 Всего товаров в базе: {total_products}')

    def _find_category_for_product(self, product_data, producer):
        """Находит подходящую категорию для товара"""
        name = product_data.get('itemNameRus') or product_data.get('itemName', '').lower()
        
        # Словарь ключевых слов для категорий
        category_keywords = {
            'Телевизоры': ['телевизор', 'tv', 'телевизоры', 'ультра', 'oled', 'qled', 'led', 'smart tv'],
            'Холодильники': ['холодильник', 'рефрижератор', 'морозильник', 'no frost', 'side by side'],
            'Стиральные машины': ['стиральная', 'стиралка', 'washing', 'автомат', 'сушильная'],
            'Плиты': ['плита', 'варочная', 'духовка', 'газовая', 'электрическая', 'индукционная'],
            'Микроволновые печи': ['микроволновка', 'свч', 'микроволновая'],
            'Пылесосы': ['пылесос', 'vacuum', 'робот-пылесос'],
            'Кофеварки и кофемашины': ['кофеварка', 'кофемашина', 'эспрессо', 'капуччино', 'кофе'],
            'Электрические чайники': ['чайник', 'электрический чайник', 'kettle'],
            'Утюги': ['утюг', 'iron', 'паровой'],
            'Блендеры': ['блендер', 'blender', 'измельчитель'],
            'Мониторы': ['монитор', 'display', 'экран'],
            'Ноутбуки': ['ноутбук', 'laptop', 'ультрабук'],
        }
        
        for category_name, keywords in category_keywords.items():
            if any(keyword in name for keyword in keywords):
                category = Category.objects.filter(name=category_name).first()
                if category:
                    return category
        
        # Если не нашли по ключевым словам, используем общую категорию
        return Category.objects.filter(name='Бытовая техника и электроника').first()