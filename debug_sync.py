import os
import django
import logging

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from catalog.models import PartnerProduct
from catalog.ocs_client import OCSClient

def debug_sync():
    ocs_client = OCSClient()
    
    # Пробуем найти товар
    try:
        product = PartnerProduct.objects.get(product_key="1000562330")
        print(f"✅ Товар найден: {product.name}")
        print(f"Product Key: {product.product_key}")
        print(f"OCS Item ID: {product.ocs_item_id}")
        print(f"Есть изображения: {product.uploaded_images.exists()}")
        print(f"Content Images: {product.content_images}")
        
        # Проверим доступ к OCS API
        print("\n1. Проверяем доступ к OCS API...")
        item_id = product.ocs_item_id or product.product_key
        print(f"Используем Item ID: {item_id}")
        
        content_data = ocs_client.get_product_content(item_id)
        print(f"Получены данные: {bool(content_data)}")
        
        if content_data:
            print(f"Количество элементов в результате: {len(content_data)}")
            for i, item in enumerate(content_data):
                if item:
                    print(f"Элемент {i}:")
                    print(f"  - ItemId: {item.get('itemId')}")
                    print(f"  - PartNumber: {item.get('partNumber')}")
                    print(f"  - Medium Images: {len(item.get('mediumImages', []))}")
                    print(f"  - Regular Images: {len(item.get('images', []))}")
                    
                    # Покажем первые 2 URL изображений
                    medium_images = item.get('mediumImages', [])
                    if medium_images:
                        print("  Medium Images URLs:")
                        for img in medium_images[:2]:
                            print(f"    - {img.get('url')}")
                    
                    regular_images = item.get('images', [])
                    if regular_images:
                        print("  Regular Images URLs:")
                        for img in regular_images[:2]:
                            print(f"    - {img.get('url')}")
                else:
                    print(f"Элемент {i}: None")
        else:
            print("❌ Не удалось получить данные из OCS API")
            
        # Попробуем синхронизацию
        print("\n2. Запускаем синхронизацию...")
        success = ocs_client.sync_product_images(product)
        print(f"Результат синхронизации: {success}")
        
    except PartnerProduct.DoesNotExist:
        print("❌ Товар с product_key='1000562330' не найден!")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    debug_sync()