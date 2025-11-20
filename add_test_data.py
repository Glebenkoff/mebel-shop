import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

import django
django.setup()

from catalog.models import Category, Product

print("📦 ДОБАВЛЕНИЕ ТЕСТОВЫХ ДАННЫХ")
print("=" * 40)

try:
    # Создаем категории
    category, created = Category.objects.get_or_create(
        name="Мягкая мебель",
        slug="myagkaya-mebel"
    )
    if created:
        print("✅ Создана категория: Мягкая мебель")
    
    # Создаем тестовый товар
    product, created = Product.objects.get_or_create(
        category=category,
        name="Диван угловой",
        slug="divan-uglovoy",
        description="Комфортный угловой диван для гостиной",
        price=29999.00,
        available=True
    )
    if created:
        print("✅ Создан товар: Диван угловой")
    
    # Проверяем количество товаров
    products_count = Product.objects.count()
    categories_count = Category.objects.count()
    
    print(f"\n📊 В базе данных:")
    print(f"   🪑 Товаров: {products_count}")
    print(f"   📁 Категорий: {categories_count}")
    
    print("\n🎉 Тестовые данные добавлены!")
    
except Exception as e:
    print(f"❌ Ошибка при добавлении данных: {e}")
