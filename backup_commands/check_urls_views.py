# management/commands/check_urls_views.py
from django.core.management.base import BaseCommand
from django.urls import get_resolver
from catalog import views

class Command(BaseCommand):
    help = 'Проверка URLs и Views'

    def handle(self, *args, **options):
        print("=== ПРОВЕРКА URLS И VIEWS ===\n")
        
        # Получаем все URLs
        resolver = get_resolver()
        url_patterns = []
        
        def get_urls(url_patterns, prefix=''):
            for pattern in url_patterns:
                if hasattr(pattern, 'url_patterns'):
                    # Это include
                    get_urls(pattern.url_patterns, prefix + pattern.pattern.regex.pattern)
                else:
                    # Это обычный pattern
                    url_patterns.append({
                        'pattern': prefix + pattern.pattern.regex.pattern,
                        'name': getattr(pattern, 'name', 'No name'),
                        'callback': pattern.callback.__name__ if hasattr(pattern, 'callback') else 'No callback'
                    })
        
        get_urls(resolver.url_patterns)
        
        print("📋 ВСЕ URLS:")
        for url in url_patterns[:20]:  # Покажем первые 20
            if 'catalog' in url['pattern'] or 'api' in url['pattern'] or url['pattern'] in ['/', '/admin/']:
                print(f"   {url['pattern']:30} -> {url['callback']:20} ({url['name']})")