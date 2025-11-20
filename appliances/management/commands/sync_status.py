# appliances/management/commands/sync_status.py
@"
from django.core.management.base import BaseCommand
from appliances.models import ApplianceProduct, ApplianceCategory
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Статус синхронизации техники'
    
    def handle(self, *args, **options):
        self.stdout.write('=== СТАТУС СИНХРОНИЗАЦИИ ТЕХНИКИ ===')
        
        # Статистика по категориям
        categories_count = ApplianceCategory.objects.count()
        products_count = ApplianceProduct.objects.count()
        active_products = ApplianceProduct.objects.filter(is_active=True).count()
        
        self.stdout.write(f'📁 Категории: {categories_count}')
        self.stdout.write(f'🛍️ Всего товаров: {products_count}')
        self.stdout.write(f'📦 Активных товаров: {active_products}')
        self.stdout.write(f'📊 В наличии: {ApplianceProduct.objects.filter(in_stock=True).count()}')
        
        # Время последней синхронизации
        recent_products = ApplianceProduct.objects.filter(
            last_sync_date__gte=timezone.now() - timedelta(hours=24)
        )
        self.stdout.write(f'🕒 Обновлено за 24ч: {recent_products.count()}')
        
        # Статистика по брендам
        from django.db.models import Count
        brands = ApplianceProduct.objects.values('brand').annotate(
            count=Count('id')
        ).filter(brand__isnull=False).order_by('-count')[:10]
        
        self.stdout.write('🏷️ Топ брендов:')
        for brand in brands:
            self.stdout.write(f'   {brand[\"brand\"]}: {brand[\"count\"]} товаров')
        
        self.stdout.write(self.style.SUCCESS('Статус проверен!'))
"@ | Out-File appliances\management\commands\sync_status.py -Encoding utf8