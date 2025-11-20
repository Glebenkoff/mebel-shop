# catalog/management/commands/check_urls_fix.py
from django.core.management.base import BaseCommand
from django.urls import get_resolver

class Command(BaseCommand):
    help = 'Проверка исправления URL конфликтов'

    def handle(self, *args, **options):
        self.stdout.write('🔗 Проверка URL на конфликты...')
        
        try:
            from catalog.urls import urlpatterns
            url_patterns = {}
            
            for pattern in urlpatterns:
                path_str = str(pattern.pattern)
                if path_str in url_patterns:
                    self.stdout.write(self.style.ERROR(
                        f'❌ КОНФЛИКТ: {path_str} -> {url_patterns[path_str]} И {pattern.name}'
                    ))
                else:
                    url_patterns[path_str] = pattern.name
                    self.stdout.write(self.style.SUCCESS(f'✅ {path_str} -> {pattern.name}'))
            
            # Проверка корневого пути
            if '' in url_patterns:
                self.stdout.write(self.style.SUCCESS(f'✅ Корневой путь: {url_patterns[""]}'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка: {e}'))