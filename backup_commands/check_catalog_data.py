from django.core.management.base import BaseCommand
from catalog.models import Category, PartnerProduct

class Command(BaseCommand):
    help = 'Проверяет данные для каталога'

    def handle(self, *args, **options):
        self.stdout.write('=== ПРОВЕРКА ДАННЫХ КАТАЛОГА ===')
        
        # Проверяем категории
        main_categories = Category.objects.filter(parent__isnull=True, category_type='main')
        self.stdout.write(f'\n📂 ОСНОВНЫЕ КАТЕГОРИИ ({main_categories.count()}):')
        for cat in main_categories:
            product_count = PartnerProduct.objects.filter(category=cat).count()
            self.stdout.write(f'  - {cat.name} (slug: {cat.slug}) - товаров: {product_count}')
            
            # Подкатегории
            for subcat in cat.children.all()[:3]:
                sub_count = PartnerProduct.objects.filter(category=subcat).count()
                self.stdout.write(f'    • {subcat.name} - товаров: {sub_count}')
        
        # Проверяем товары
        total_products = PartnerProduct.objects.count()
        self.stdout.write(f'\n📦 ВСЕГО ТОВАРОВ: {total_products}')
        
        if total_products > 0:
            self.stdout.write('\n📋 ПЕРВЫЕ 5 ТОВАРОВ:')
            for product in PartnerProduct.objects.all()[:5]:
                category_name = product.category.name if product.category else 'Нет категории'
                self.stdout.write(f'  - {product.name}')
                self.stdout.write(f'    💰 {product.price} ₽ | 🏷️ {product.producer} | 📁 {category_name}')
        
        # Проверяем view функцию
        self.stdout.write('\n🔧 ПРОВЕРКА VIEW:')
        from django.test import RequestFactory
        from catalog.views import catalog_view
        
        factory = RequestFactory()
        request = factory.get('/catalog/')
        
        # Имитируем вызов view
        try:
            response = catalog_view(request)
            self.stdout.write('✅ View функция работает корректно')
        except Exception as e:
            self.stdout.write(f'❌ Ошибка в view: {e}')