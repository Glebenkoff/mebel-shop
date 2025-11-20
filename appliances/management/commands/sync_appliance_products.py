from django.core.management.base import BaseCommand
from appliances.services.ocs_sync_service import OCSSyncService

class Command(BaseCommand):
    help = 'Синхронизация товаров техники с OCS API'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--category-limit',
            type=int,
            default=5,
            help='имит категорий для синхронизации (по умолчанию: 5)'
        )
    
    def handle(self, *args, **options):
        category_limit = options['category_limit']
        
        self.stdout.write(f'=== СХЯ Т ТХ (лимит: {category_limit}) ===')
        
        sync_service = OCSSyncService()
        products_count = sync_service.sync_products(category_limit)
        
        if products_count > 0:
            self.stdout.write(
                self.style.SUCCESS(f'спешно синхронизировано товаров: {products_count}')
            )
        else:
            self.stdout.write(
                self.style.WARNING('ет новых товаров для синхронизации')
            )
