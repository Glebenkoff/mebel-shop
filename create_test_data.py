import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

import django
django.setup()

from catalog.models import Category, Product

print("🔄 Создаем тестовые данные...")

# Очищаем старые данные
Product.objects.all().delete()
Category.objects.all().delete()

# Создаем категории
categories = [
    {'name': 'Диваны', 'slug': 'divany'},
    {'name': 'Столы', 'slug': 'stoly'},
]

for cat_data in categories:
    category = Category.objects.create(**cat_data)
    print(f"✅ Категория: {category.name}")

# Создаем товары
products = [
    {'name': 'Диван угловой', 'slug': 'divan-uglovoy', 'price': 29999, 'category': Category.objects.get(name='Диваны')},
    {'name': 'Диван прямой', 'slug': 'divan-pryamoy', 'price': 19999, 'category': Category.objects.get(name='Диваны')},
    {'name': 'Обеденный стол', 'slug': 'obedenny-stol', 'price': 12999, 'category': Category.objects.get(name='Столы')},
]

for prod_data in products:
    product = Product.objects.create(**prod_data)
    print(f"✅ Товар: {product.name} - {product.price} ₽")

print("🎉 Готово!")
