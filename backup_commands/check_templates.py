# catalog/management/commands/check_templates.py
from django.core.management.base import BaseCommand
import os

class Command(BaseCommand):
    help = 'Проверка существующих шаблонов'

    def handle(self, *args, **options):
        self.stdout.write('🔍 Проверка существующих шаблонов...')
        
        templates_to_check = [
            'main/home.html',
            'catalog/catalog.html',
            'base.html',
            'catalog/product_detail.html', 
            'cart/detail.html'
        ]
        
        for template in templates_to_check:
            template_path = os.path.join('templates', template)
            if os.path.exists(template_path):
                self.stdout.write(self.style.SUCCESS(f'✅ {template} - СУЩЕСТВУЕТ'))
                # Покажем размер файла
                size = os.path.getsize(template_path)
                self.stdout.write(f'   Размер: {size} байт')
            else:
                self.stdout.write(self.style.WARNING(f'❌ {template} - ОТСУТСТВУЕТ'))