from django.core.management.base import BaseCommand
from catalog.models import PartnerProduct, ProductImage
from catalog.ocs_client import OCSClient
import time

class Command(BaseCommand):
    help = 'Синхронизация изображений товаров из OCS'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--batch-size',
            type=int,
            default=50,
            help='Размер батча для запросов к API'
        )
        parser.add_argument(
            '--delay',
            type=float,
            default=0.5,
            help='Задержка между запросами (секунды)'
        )
        parser.add_argument(
            '--product-ids',
            type=str,
            help='ID товаров через запятую для выборочной синхронизации'
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Синхронизировать все товары (даже с изображениями)'
        )
    
    def handle(self, *args, **options):
        ocs_client = OCSClient()
        batch_size = options['batch_size']
        delay = options['delay']
        
        # Определяем какие товары синхронизировать
        if options['product_ids']:
            product_ids = [pid.strip() for pid in options['product_ids'].split(',')]
            products = PartnerProduct.objects.filter(product_key__in=product_ids)
            self.stdout.write(f"Выборочная синхронизация {len(products)} товаров")
        elif options['all']:
            # Все товары
            products = PartnerProduct.objects.all()[:1000]
            self.stdout.write(f"Синхронизация всех товаров: {products.count()}")
        else:
            # Только товары без изображений
            products = PartnerProduct.objects.filter(
                uploaded_images__isnull=True
            )[:1000]
            self.stdout.write(f"Найдено товаров без изображений: {products.count()}")
        
        if not products:
            self.stdout.write(self.style.SUCCESS("✅ Все товары уже имеют изображения!"))
            return
        
        total_processed = 0
        total_success = 0
        
        for product in products:
            self.stdout.write(f"Обрабатываем: {product.name}")
            
            success = ocs_client.sync_product_images(product)
            
            if success:
                total_success += 1
                self.stdout.write(self.style.SUCCESS(f"✅ Успешно: {product.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"⚠️ Пропущено: {product.name}"))
            
            total_processed += 1
            
            # Задержка чтобы не превысить лимиты API
            time.sleep(delay)
            
            # Прогресс каждые 10 товаров
            if total_processed % 10 == 0:
                self.stdout.write(f"Обработано: {total_processed}/{len(products)}")
        
        self.stdout.write(
            self.style.SUCCESS(
                f"✅ Синхронизация завершена! Успешно: {total_success}/{total_processed}"
            )
        )
    
    def process_product_content(self, product_content, ocs_client):
        """Обработка контента одного товара"""
        item_id = product_content.get('itemId')
        
        try:
            product = PartnerProduct.objects.get(
                ocs_item_id=item_id
            )
            
            # Очищаем старые изображения
            product.uploaded_images.all().delete()
            
            # Обрабатываем основные изображения
            images = product_content.get('images', [])
            medium_images = product_content.get('mediumImages', [])
            
            # Используем medium images (800x800) как основные
            for order, image_data in enumerate(medium_images[:5]):  # максимум 5 изображений
                image_url = image_data.get('url')
                if image_url:
                    ocs_client.download_image(image_url, product.product_key)
            
            # Если нет medium images, используем обычные
            if not medium_images and images:
                for order, image_data in enumerate(images[:5]):
                    image_url = image_data.get('url')
                    if image_url:
                        ocs_client.download_image(image_url, product.product_key)
            
            self.stdout.write(
                self.style.SUCCESS(f'✅ Загружены изображения для {product.name}')
            )
            
        except PartnerProduct.DoesNotExist:
            self.stdout.write(
                self.style.WARNING(f'⚠️ Товар с itemId {item_id} не найден в базе')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Ошибка обработки товара {item_id}: {e}')
            )