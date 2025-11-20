# management/commands/check_views.py
from django.core.management.base import BaseCommand
from django.urls import reverse, resolve
from catalog import views

class Command(BaseCommand):
    help = 'Проверка views и URLs'

    def handle(self, *args, **options):
        print("=== ПРОВЕРКА VIEWS И URLS ===\n")
        
        # Проверяем основные URLs
        urls_to_check = [
            ('/', 'Главная'),
            ('/catalog/', 'Каталог'),
            ('/api/products/', 'API товаров'),
        ]
        
        for url, name in urls_to_check:
            try:
                match = resolve(url)
                print(f"📌 {name}:")
                print(f"   URL: {url}")
                print(f"   View: {match.func.__name__}")
                print(f"   App: {match.app_name}")
                print()
            except Exception as e:
                print(f"❌ {name}: {url} - {e}\n")