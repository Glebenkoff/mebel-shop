from django.core.management.base import BaseCommand
from appliances.services.ocs_sync_service import OCSSyncService

class Command(BaseCommand):
    help = 'Синхронизация категорий техники с OCS API'
    
    def handle(self, *args, **options):
        self.stdout.write('=== СХЯ Т ТХ ===')
        
        sync_service = OCSSyncService()
        categories_count = sync_service.sync_categories()
        
        if categories_count > 0:
            self.stdout.write(
                self.style.SUCCESS(f'спешно синхронизировано категорий: {categories_count}')
            )
        else:
            self.stdout.write(
                self.style.WARNING('ет новых категорий для синхронизации')
            )
