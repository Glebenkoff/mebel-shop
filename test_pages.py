import requests
import time

def test_pages():
    base_url = "http://localhost:8000"
    pages = [
        "/",
        "/admin/",
        "/catalog/",
        "/cart/",
        "/accounts/login/",
        "/pages/about/"
    ]
    
    print("🌐 ТЕСТИРОВАНИЕ СТРАНИЦ")
    print("=" * 40)
    
    for page in pages:
        try:
            response = requests.get(base_url + page, timeout=5)
            status = "✅" if response.status_code == 200 else "⚠️ "
            print(f"{status} {page}: {response.status_code}")
        except Exception as e:
            print(f"❌ {page}: недоступно ({e})")
    
    print("\n🎉 ТЕСТИРОВАНИЕ ЗАВЕРШЕНО!")

if __name__ == '__main__':
    test_pages()
