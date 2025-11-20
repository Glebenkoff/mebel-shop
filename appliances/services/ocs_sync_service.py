import logging
from django.utils import timezone
from appliances.models import ApplianceCategory, ApplianceProduct
from appliances.services.ocs_api_service import OCSApiService

logger = logging.getLogger(__name__)

class OCSSyncService:
    # Сервис синхронизации с OCS API
    
    def __init__(self):
        self.api_service = OCSApiService()
    
    def sync_categories(self):
        # Синхронизация категорий
        logger.info('ачало синхронизации категорий')
        
        categories_data = self.api_service.get_categories()
        if not categories_data:
            logger.error('е удалось получить категории')
            return 0
        
        tech_categories = self._extract_technology_categories(categories_data)
        saved_count = 0
        
        for category_data in tech_categories:
            category, created = ApplianceCategory.objects.get_or_create(
                code=category_data['category'],
                defaults={
                    'name': category_data.get('name', ''),
                }
            )
            if created:
                saved_count += 1
        
        logger.info(f'Синхронизировано категорий: {saved_count}')
        return saved_count
    
    def sync_products(self, category_limit=5):
        # Синхронизация товаров
        logger.info('ачало синхронизации товаров')
        
        tech_categories = ApplianceCategory.objects.all()[:category_limit]
        total_products = 0
        
        for category in tech_categories:
            logger.info(f'Синхронизация категории: {category.name}')
            
            products_data = self.api_service.get_category_products(category.code)
            if not products_data:
                continue
            
            if isinstance(products_data, dict) and 'result' in products_data:
                products_list = products_data['result']
                category_products_count = 0
                
                for product_item in products_list:
                    product_data = product_item.get('product', {})
                    
                    product, created = ApplianceProduct.objects.update_or_create(
                        item_id=product_data.get('itemId'),
                        defaults={
                            'product_key': product_data.get('productKey', ''),
                            'part_number': product_data.get('partNumber', ''),
                            'name': product_data.get('itemName', ''),
                            'russian_name': product_data.get('itemNameRus', ''),
                            'product_name': product_data.get('productName', ''),
                            'description': product_data.get('productDescription', ''),
                            'category': category,
                            'producer': product_data.get('producer', ''),
                            'brand': product_data.get('brand', ''),
                            'stock': product_data.get('stock', 0),
                            'warranty': product_data.get('warranty', ''),
                            'line_code': product_data.get('lineCode', ''),
                            'ean128': product_data.get('eaN128', ''),
                            'vat_percent': product_data.get('vatPercent'),
                        }
                    )
                    
                    if created:
                        category_products_count += 1
                
                logger.info(f'атегория {category.name}: добавлено {category_products_count} товаров')
                total_products += category_products_count
        
        logger.info(f'сего синхронизировано товаров: {total_products}')
        return total_products
    
    def _extract_technology_categories(self, categories_data):
        # звлечение категорий техники (V07)
        tech_categories = []
        
        for category in categories_data:
            if category.get('category') == 'V07':
                tech_categories.append(category)
                tech_categories.extend(self._get_all_subcategories(category))
        
        return tech_categories
    
    def _get_all_subcategories(self, category):
        # екурсивное получение всех подкатегорий
        subcategories = []
        children = category.get('children', [])
        
        for child in children:
            subcategories.append(child)
            subcategories.extend(self._get_all_subcategories(child))
        
        return subcategories
