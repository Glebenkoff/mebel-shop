#!/usr/bin/env python
"""
АВТОНОМНЫЙ СКРИПТ УПРАВЛЕНИЯ ДАННЫМИ - ИСПРАВЛЕННАЯ ВЕРСИЯ
Для проекта с настройками в корневой папке
"""

import os
import sys
import django
import argparse
import logging
import json
from pathlib import Path
from datetime import datetime

# 🗂️ НАСТРОЙКА ПУТЕЙ ДЛЯ ПРОЕКТА С НАСТРОЙКАМИ В КОРНЕ
BASE_DIR = Path(__file__).resolve().parent
print(f"📍 Папка проекта: {BASE_DIR}")

# 📁 Добавляем папку проекта в Python path
sys.path.insert(0, str(BASE_DIR))

# 🗂️ Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(BASE_DIR / 'data_manager.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('data_manager')

def setup_django():
    """
    Настройка Django для проекта с настройками в корне
    """
    try:
        # 🎯 ИСПРАВЛЕНИЕ: используем 'settings' вместо 'mebel_shop.settings'
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
        print("🔄 Настройка Django...")
        
        django.setup()
        logger.info("✅ Django настроен успешно!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Ошибка настройки Django: {e}")
        return False

def show_statistics():
    """Показать статистику данных"""
    logger.info("📊 ЗАГРУЗКА СТАТИСТИКИ...")
    
    try:
        from catalog.models import Category, Product, Coupon
        from cart.models import Cart, CartItem
        from accounts.models import CustomUser
        
        stats = {
            'Категории': Category.objects.count(),
            'Товары': Product.objects.count(),
            'Купоны': Coupon.objects.count(),
            'Пользователи': CustomUser.objects.count(),
            'Корзины': Cart.objects.count(),
            'Элементы корзин': CartItem.objects.count()
        }
        
        print("\n" + "="*50)
        print("📈 СТАТИСТИКА МАГАЗИНА")
        print("="*50)
        
        for item, count in stats.items():
            print(f"  {item}: {count}")
            
        print("="*50)
        
        # 📦 Детальная информация о товарах
        products = Product.objects.all()[:5]
        if products:
            print("\n📦 ПОСЛЕДНИЕ ТОВАРЫ:")
            for product in products:
                print(f"  • {product.name} - {product.price} руб.")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Ошибка загрузки статистики: {e}")
        import traceback
        traceback.print_exc()
        return False

def create_test_data():
    """Создание тестовых данных"""
    logger.info("🧪 СОЗДАНИЕ ТЕСТОВЫХ ДАННЫХ...")
    
    try:
        from catalog.models import Category, Product
        
        # Создаем тестовую категорию
        category, created = Category.objects.get_or_create(
            name="Тестовая мебель",
            defaults={'description': 'Категория для тестирования системы'}
        )
        
        if created:
            logger.info(f"✅ Создана категория: {category.name}")
        else:
            logger.info(f"ℹ️ Категория уже существует: {category.name}")
        
        # Создаем тестовый товар
        product, created = Product.objects.get_or_create(
            name="Тестовый диван",
            defaults={
                'category': category,
                'price': 15000.00,
                'description': 'Комфортный диван для гостиной',
                'stock': 5
            }
        )
        
        if created:
            logger.info(f"✅ Создан товар: {product.name} - {product.price} руб.")
        else:
            logger.info(f"ℹ️ Товар уже существует: {product.name}")
            
        return True
        
    except Exception as e:
        logger.error(f"❌ Ошибка создания тестовых данных: {e}")
        return False

def backup_data():
    """Создание резервной копии данных"""
    logger.info("💾 СОЗДАНИЕ РЕЗЕРВНОЙ КОПИИ...")
    
    try:
        # Создаем папку для бэкапов
        backup_dir = BASE_DIR / 'backups'
        backup_dir.mkdir(exist_ok=True)
        
        # Создаем файл бэкапа
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = backup_dir / f'backup_{timestamp}.json'
        
        backup_data = {
            'timestamp': timestamp,
            'project': 'Furniture Store',
            'data': {}
        }
        
        # Сохраняем категории
        from catalog.models import Category
        categories = list(Category.objects.values('id', 'name', 'description'))
        backup_data['data']['categories'] = categories
        
        # Сохраняем товары
        from catalog.models import Product
        products = list(Product.objects.values('id', 'name', 'price', 'description', 'stock'))
        backup_data['data']['products'] = products
        
        # Записываем в JSON
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"✅ Резервная копия создана: {backup_file}")
        logger.info(f"   📁 Категорий: {len(categories)}")
        logger.info(f"   📦 Товаров: {len(products)}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Ошибка создания резервной копии: {e}")
        return False

def main():
    """Основная функция"""
    parser = argparse.ArgumentParser(description='Автономный менеджер данных магазина')
    parser.add_argument('command', choices=['статистика', 'тест', 'резервная_копия', 'все'],
                       help='Команда для выполнения')
    
    args = parser.parse_args()
    
    print("🚀 АВТОНОМНЫЙ МЕНЕДЖЕР ДАННЫХ")
    print("📍 Структура: настройки в корневой папке")
    print("="*60)
    
    # Настраиваем Django
    if not setup_django():
        print("❌ Не удалось настроить Django")
        return
    
    # Выполняем команды
    success = True
    
    if args.command == 'статистика':
        success = show_statistics()
    elif args.command == 'тест':
        success = create_test_data()
    elif args.command == 'резервная_копия':
        success = backup_data()
    elif args.command == 'все':
        success = show_statistics() and create_test_data() and backup_data()
    
    if success:
        print("\n✅ ВЫПОЛНЕНИЕ ЗАВЕРШЕНО УСПЕШНО")
    else:
        print("\n⚠️ ВЫПОЛНЕНИЕ ЗАВЕРШЕНО С ОШИБКАМИ")
    
    print(f"📋 Подробности в: {BASE_DIR}/data_manager.log")

if __name__ == "__main__":
    main()