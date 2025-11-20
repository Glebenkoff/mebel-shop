#!/usr/bin/env python
"""
ПРОСТОЙ ТЕСТОВЫЙ СКРИПТ
Проверка базовой функциональности
"""

import os
import sys
from pathlib import Path

# Настройка Django
BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

print("🧪 ПРОСТОЙ ТЕСТ DJANGO")
print("="*40)

try:
    import django
    django.setup()
    print("✅ Django настроен!")
    
    # Тест моделей
    from catalog.models import Category, Product
    
    categories = Category.objects.count()
    products = Product.objects.count()
    
    print(f"📊 Категории: {categories}")
    print(f"📦 Товары: {products}")
    
    if products > 0:
        print("\n📝 Примеры товаров:")
        for product in Product.objects.all()[:3]:
            print(f"  • {product.name} - {product.price} руб.")
    
    print("\n🎯 ТЕСТ ПРОЙДЕН УСПЕШНО!")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()