# management/commands/check_catalog_simple.py
from django.core.management.base import BaseCommand
from catalog.models import Category, PartnerProduct

class Command(BaseCommand):
    help = 'Простая проверка данных каталога'

    def handle(self, *args, **options):
        print("=== ПРОВЕРКА ДАННЫХ КАТАЛОГА ===")
        
        # Основные категории (те, у которых нет родителя)
        main_categories = Category.objects.filter(parent__isnull=True)
        
        print(f"\n📂 ОСНОВНЫЕ КАТЕГОРИИ ({main_categories.count()}):")
        
        for main_cat in main_categories:
            # Считаем товары только в этой категории (без учета подкатегорий)
            products_in_main_cat = PartnerProduct.objects.filter(category=main_cat).count()
            
            print(f"  - {main_cat.name} (slug: {main_cat.slug}) - товаров: {products_in_main_cat}")
            
            # Показываем подкатегории первого уровня
            subcategories = Category.objects.filter(parent=main_cat)[:3]  # только первые 3
            for subcat in subcategories:
                subcat_products_count = PartnerProduct.objects.filter(category=subcat).count()
                print(f"    • {subcat.name} - товаров: {subcat_products_count}")
            
            if subcategories.count() > 3:
                print(f"    • ... и еще {subcategories.count() - 3} подкатегорий")
        
        # Общая статистика
        total_products = PartnerProduct.objects.count()
        products_with_price = PartnerProduct.objects.exclude(price=0).count()
        
        print(f"\n📊 СТАТИСТИКА:")
        print(f"📦 Всего товаров: {total_products}")
        print(f"💰 Товаров с ценой: {products_with_price}")
        print(f"❌ Товаров без цены: {total_products - products_with_price}")
        
        # Категории с товарами
        categories_with_products = Category.objects.filter(
            partnerproduct__isnull=False
        ).distinct()
        
        print(f"\n🏷️ КАТЕГОРИИ С ТОВАРАМИ ({categories_with_products.count()}):")
        for cat in categories_with_products:
            count = PartnerProduct.objects.filter(category=cat).count()
            print(f"  - {cat.name}: {count} товаров")
        
        # Первые 5 товаров
        print(f"\n📋 ПЕРВЫЕ 5 ТОВАРОВ:")
        products = PartnerProduct.objects.all()[:5]
        for product in products:
            price_display = f"{product.price} ₽" if product.price else "❌ НЕТ ЦЕНЫ"
            brand_display = product.brand if product.brand else "Не указан"
            print(f"  - {product.name}")
            print(f"    💰 {price_display} | 🏷️ {brand_display} | 📁 {product.category}")
        
        print(f"\n✅ Проверка завершена успешно!")