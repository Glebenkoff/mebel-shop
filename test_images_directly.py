import os
import django
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.conf import settings

def test_image_urls():
    base_url = settings.OCS_API_URL
    api_key = settings.OCS_API_KEY
    
    # Тестовые URL из вашего вывода
    test_urls = [
        "https://testconnector.b2b.ocs.ru/api/v2/files/mediumimages/A7310874-B26D-4692-9077-8A36FC072FA5.jpg",
        "https://testconnector.b2b.ocs.ru/api/v2/files/mediumimages/5EF52139-3A35-4BFB-AA1A-3FB9296DA62E.jpg",
        "https://testconnector.b2b.ocs.ru/api/v2/files/contentimages/A7310874-B26D-4692-9077-8A36FC072FA5.jpg",
        "https://testconnector.b2b.ocs.ru/api/v2/files/contentimages/5EF52139-3A35-4BFB-AA1A-3FB9296DA62E.jpg"
    ]
    
    headers = {"X-API-Key": api_key}
    
    for url in test_urls:
        print(f"\nТестируем: {url}")
        try:
            # Сначала HEAD запрос чтобы проверить доступность
            head_response = requests.head(url, headers=headers, timeout=10)
            print(f"HEAD Status: {head_response.status_code}")
            
            if head_response.status_code == 200:
                # Пробуем GET запрос
                get_response = requests.get(url, headers=headers, timeout=30, stream=True)
                print(f"GET Status: {get_response.status_code}")
                print(f"Content-Type: {get_response.headers.get('content-type', 'Unknown')}")
                print(f"Content-Length: {get_response.headers.get('content-length', 'Unknown')}")
                
                if get_response.status_code == 200:
                    print("✅ Изображение доступно для скачивания")
                else:
                    print(f"❌ Ошибка GET: {get_response.text[:100]}")
            else:
                print(f"❌ HEAD запрос не удался")
                
        except Exception as e:
            print(f"❌ Исключение: {e}")

if __name__ == "__main__":
    test_image_urls()