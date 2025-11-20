from django.core.management.base import BaseCommand
from appliances.services.ocs_sync_service import OCSSyncService

class Command(BaseCommand):
    help = 'олная синхронизация техники с OCS API'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--category-limit',
            type=int,
            default=5,
            help='имит категорий для синхронизации товаров (по умолчанию: 5)'
        )
    
    def handle(self, *args, **options):
        category_limit = options['category_limit']
        
        self.stdout.write('=== Я СХЯ ТХ ===')
        
        sync_service = OCSSyncService()
        
        # Синхронизация категорий
        self.stdout.write('1. Синхронизация категорий...')
        categories_count = sync_service.sync_categories()
        self.stdout.write(f'   Синхронизировано категорий: {categories_count}')
        
        # Синхронизация товаров
        self.stdout.write('2. Синхронизация товаров...')
        products_count = sync_service.sync_products(category_limit)
        self.stdout.write(f'   Синхронизировано товаров: {products_count}')
        
        self.stdout.write(
            self.style.SUCCESS(f'олная синхронизация завершена! атегории: {categories_count}, Товары: {products_count}')
        )
