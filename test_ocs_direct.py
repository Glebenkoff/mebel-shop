# test_ocs_direct.py
import os
import django
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.conf import settings

def test_ocs_api_directly():
    base_url = settings.OCS_API_URL
    api_key = settings.OCS_API_KEY
    item_id = "1000562330"  # ID товара
    
    print(f"Тестируем прямой запрос к OCS API")
    print(f"URL: {base_url}")
    print(f"Item ID: {item_id}")
    
    # Тест 1: Получение контента товара
    url = f"{base_url}/api/v2/content/{item_id}"
    headers = {
        "X-API-Key": api_key,
        "accept": "application/json"
    }
    
    print(f"\n1. Запрос контента товара...")
    print(f"URL: {url}")
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Успешно!")
            if 'result' in data and data['result']:
                product_data = data['result'][0]
                print(f"ItemId: {product_data.get('itemId')}")
                print(f"PartNumber: {product_data.get('partNumber')}")
                print(f"Medium Images: {len(product_data.get('mediumImages', []))}")
                print(f"Regular Images: {len(product_data.get('images', []))}")
                
                # Показать URL изображений
                medium_images = product_data.get('mediumImages', [])
                if medium_images:
                    print("\nMedium Images URLs:")
                    for img in medium_images[:3]:
                        print(f"  - {img.get('url')}")
            else:
                print("❌ Нет данных в результате")
        else:
            print(f"❌ Ошибка: {response.text}")
            
    except Exception as e:
        print(f"❌ Исключение: {e}")

if __name__ == "__main__":
    test_ocs_api_directly()