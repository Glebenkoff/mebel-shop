from django.core.management.base import BaseCommand
from catalog.services.ocs_sync_service import OcsSyncService
import time

class Command(BaseCommand):
    help = 'Синхронизация товаров с OCS API'

    def add_arguments(self, parser):
        parser.add_argument(
            '--delay',
            type=float,
            default=1.0,
            help='Задержка между запросами (по умолчанию 1.0 сек)'
        )

    def handle(self, *args, **options):
        delay = options['delay']
        
        self.stdout.write("🔄 Запуск синхронизации товаров с OCS...")
        
        try:
            sync_service = OcsSyncService()
            results = sync_service.sync_all_products(delay=delay)
            
            self.stdout.write(
                self.style.SUCCESS(
                    f"✅ Синхронизация завершена! "
                    f"Обработано: {results['processed']}, "
                    f"Создано: {results['created']}, "
                    f"Обновлено: {results['updated']}, "
                    f"Ошибки: {results['errors']}"
                )
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Ошибка синхронизации: {str(e)}")
            )