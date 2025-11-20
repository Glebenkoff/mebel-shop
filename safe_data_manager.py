#!/usr/bin/env python
"""
БЕЗОПАСНЫЙ МЕНЕДЖЕР ДАННЫХ - обход проблемных файлов
"""

import os
import sys
from pathlib import Path

print("🛡️ БЕЗОПАСНЫЙ МЕНЕДЖЕР ДАННЫХ")
print("="*50)

BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR))

# Минимальная настройка Django БЕЗ автоматического импорта
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

try:
    import django
    from django.conf import settings
    
    # Настраиваем Django вручную
    if not settings.configured:
        settings._setup()
    
    django.setup()
    print("✅ Django настроен безопасно!")
    
except Exception as e:
    print(f"❌ Ошибка настройки Django: {e}")
    sys.exit(1)

def safe_import_models():
    """Безопасный импорт моделей с обработкой ошибок"""
    print("\n📦 БЕЗОПАСНЫЙ ИМПОРТ МОДЕЛЕЙ:")
    
    models_to_import = [
        ('catalog.models', ['Category', 'Product', 'Coupon']),
        ('cart.models', ['Cart', 'CartItem']),
        ('accounts.models', ['CustomUser']),
    ]
    
    imported_models = {}
    
    for module_path, model_names in models_to_import:
        print(f"\n🔍 Модуль: {module_path}")
        
        try:
            # Пробуем импортировать весь модуль
            module = __import__(module_path, fromlist=model_names)
            print(f"   ✅ Модуль загружен")
            
            # Пробуем получить каждую модель
            for model_name in model_names:
                try:
                    model_class = getattr(module, model_name)
                    imported_models[model_name] = model_class
                    print(f"   ✅ {model_name} - OK")
                except AttributeError:
                    print(f"   ⚠️ {model_name} - не найден")
                    
        except Exception as e:
            print(f"   ❌ Ошибка загрузки: {e}")
    
    return imported_models

def get_statistics_safe(models_dict):
    """Безопасное получение статистики"""
    print("\n📊 БЕЗОПАСНАЯ СТАТИСТИКА:")
    
    stats = {}
    
    for model_name, model_class in models_dict.items():
        try:
            count = model_class.objects.count()
            stats[model_name] = count
            print(f"   ✅ {model_name}: {count}")
        except Exception as e:
            print(f"   ❌ {model_name}: ошибка - {e}")
            stats[model_name] = None
    
    return stats

def main():
    """Основная функция"""
    # Безопасный импорт моделей
    models = safe_import_models()
    
    if not models:
        print("\n❌ Не удалось загрузить ни одной модели")
        return
    
    # Получаем статистику
    stats = get_statistics_safe(models)
    
    print("\n" + "="*50)
    print("📈 ИТОГОВАЯ СТАТИСТИКА:")
    for model_name, count in stats.items():
        if count is not None:
            print(f"   {model_name}: {count}")
    
    print("\n✅ БЕЗОПАСНЫЙ СКРИПТ ЗАВЕРШЕН")

if __name__ == "__main__":
    main()