# management/commands/check_catalog_fixed.py
from django.core.management.base import BaseCommand
from catalog.models import Category, PartnerProduct
from django.db.models import Count

class Command(BaseCommand):
    help = 'Финальная проверка данных каталога'

    def handle(self, *args, **options):
        print("=== ПРОВЕРКА ДАННЫХ КАТАЛОГА ===\n")
        
        # Основные категории (те, у которых нет родителя)
        main_categories = Category.objects.filter(parent__isnull=True)
        
        print(f"📂 ОСНОВНЫЕ КАТЕГОРИИ ({main_categories.count()}):")
        
        for main_cat in main_categories:
            # Считаем товары в основной категории
            products_in_main_cat = PartnerProduct.objects.filter(category=main_cat).count()
            
            print(f"\n  - {main_cat.name} (slug: {main_cat.slug}) - товаров: {products_in_main_cat}")
            
            # Показываем подкатегории первого уровня с товарами
            subcategories = Category.objects.filter(parent=main_cat)
            subcategories_with_products = subcategories.annotate(
                product_count=Count('products')  # ← ИСПРАВЛЕНО: было 'partnerproduct', стало 'products'
            ).filter(product_count__gt=0)
            
            for subcat in subcategories_with_products[:5]:  # только первые 5 с товарами
                print(f"    • {subcat.name} - товаров: {subcat.product_count}")
            
            if subcategories_with_products.count() > 5:
                print(f"    • ... и еще {subcategories_with_products.count() - 5} подкатегорий с товарами")
        
        # Общая статистика
        total_products = PartnerProduct.objects.count()
        products_with_price = PartnerProduct.objects.exclude(price=0).count()
        products_with_categories = PartnerProduct.objects.filter(category__isnull=False).count()
        
        print(f"\n📊 СТАТИСТИКА:")
        print(f"📦 Всего товаров: {total_products}")
        print(f"📁 Товаров с категориями: {products_with_categories}")
        print(f"🏷️ Товаров без категорий: {total_products - products_with_categories}")
        print(f"💰 Товаров с ценой: {products_with_price}")
        print(f"❌ Товаров без цены: {total_products - products_with_price}")
        
        # Категории с товарами (правильный способ)
        categories_with_products = Category.objects.annotate(
            product_count=Count('products')  # ← ИСПРАВЛЕНО
        ).filter(product_count__gt=0)
        
        print(f"\n🏷️ КАТЕГОРИИ С ТОВАРАМИ ({categories_with_products.count()}):")
        for cat in categories_with_products.order_by('-product_count')[:10]:  # топ-10
            print(f"  - {cat.name}: {cat.product_count} товаров")
        
        # Проблемные товары (без цены или категории)
        products_no_price = PartnerProduct.objects.filter(price=0)
        products_no_category = PartnerProduct.objects.filter(category__isnull=True)
        
        print(f"\n⚠️  ПРОБЛЕМНЫЕ ТОВАРЫ:")
        print(f"  - Без цены: {products_no_price.count()}")
        print(f"  - Без категории: {products_no_category.count()}")
        
        # Первые 5 товаров с деталями
        print(f"\n📋 ПЕРВЫЕ 5 ТОВАРОВ:")
        products = PartnerProduct.objects.all()[:5]
        for i, product in enumerate(products, 1):
            price_display = f"{product.price} ₽" if product.price else "❌ НЕТ ЦЕНЫ"
            brand_display = product.producer if product.producer else "Не указан"  # ← исправлено: было brand, стало producer
            category_display = product.category.name if product.category else "❌ НЕТ КАТЕГОРИИ"
            
            print(f"\n  {i}. {product.name}")
            print(f"     💰 Цена: {price_display}")
            print(f"     🏷️ Бренд: {brand_display}")
            print(f"     📁 Категория: {category_display}")
        
        print(f"\n✅ Проверка завершена успешно!")