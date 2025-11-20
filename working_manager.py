#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
РАБОТАЮЩИЙ МЕНЕДЖЕР ДАННЫХ
"""

import os
import sys
from pathlib import Path

# Настройка Django
BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

import django
django.setup()

from catalog.models import Category, Product

print("🔄 РАБОТАЮЩИЙ МЕНЕДЖЕР ДАННЫХ")
print("=" * 40)

# Создаем тестовые данные
if Category.objects.count() == 0:
    category = Category.objects.create(
        name="Мебель для гостиной",
        description="Диваны, кресла, журнальные столики"
    )
    print(f"✅ Создана категория: {category.name}")

if Product.objects.count() == 0:
    category = Category.objects.first()
    product = Product.objects.create(
        name="Комфортный диван",
        category=category,
        price=25000.00,
        description="Мягкий диван для гостиной",
        stock=5
    )
    print(f"✅ Создан товар: {product.name} - {product.price} руб.")

# Статистика
print(f"📊 Категории: {Category.objects.count()}")
print(f"📦 Товары: {Product.objects.count()}")
print("✅ ВЫПОЛНЕНИЕ ЗАВЕРШЕНО!")
