import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class OCSApiService:
    # Сервис для работы с OCS API
    
    def __init__(self):
        self.base_url = 'https://testconnector.b2b.ocs.ru'
        self.token = 'n*WpKPp-WYB5edu8P-XrDmjeyuht1K'
        self.headers = {
            'X-API-Key': self.token,
            'Content-Type': 'application/json'
        }
    
    def get_categories(self):
        # олучение дерева категорий
        try:
            response = requests.get(
                f'{self.base_url}/api/v2/catalog/categories',
                headers=self.headers
            )
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f'шибка получения категорий: {response.status_code}')
                return None
        except Exception as e:
            logger.error(f'сключение при получении категорий: {e}')
            return None
    
    def get_category_products(self, category_code):
        # олучение товаров по категории
        try:
            response = requests.get(
                f'{self.base_url}/api/v2/catalog/categories/{category_code}/products',
                headers=self.headers
            )
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f'шибка получения товаров категории {category_code}: {response.status_code}')
                return None
        except Exception as e:
            logger.error(f'сключение при получении товаров категории {category_code}: {e}')
            return None
    
    def get_product_details(self, item_ids):
        # олучение детальной информации о товарах
        try:
            if isinstance(item_ids, list):
                item_ids = ','.join(item_ids)
            
            response = requests.get(
                f'{self.base_url}/api/v2/catalog/products/{item_ids}',
                headers=self.headers
            )
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f'шибка получения деталей товаров: {response.status_code}')
                return None
        except Exception as e:
            logger.error(f'сключение при получении деталей товаров: {e}')
            return None
