#!/usr/bin/env python
"""
ОТЛАДКА ИМПОРТОВ - находим проблемный файл
"""

import os
import sys
import builtins
from pathlib import Path

# Сохраняем оригинальный import
original_import = builtins.__import__

# Счетчик импортов
import_count = 0
problem_files = []

def debug_import(name, globals=None, locals=None, fromlist=(), level=0):
    """Отладочная версия импорта"""
    global import_count
    
    try:
        # Пробуем импортировать
        result = original_import(name, globals, locals, fromlist, level)
        import_count += 1
        
        # Логируем успешные импорты Django
        if 'django' in name or any(app in name for app in ['catalog', 'cart', 'accounts']):
            print(f"✅ [{import_count}] Импорт: {name}")
            
        return result
        
    except SyntaxError as e:
        # Ловим ошибки синтаксиса (нулевые байты)
        print(f"❌ СИНТАКСИЧЕСКАЯ ОШИБКА в модуле: {name}")
        print(f"   Ошибка: {e}")
        problem_files.append(name)
        raise
    except Exception as e:
        print(f"⚠️  Ошибка импорта {name}: {e}")
        raise

# Заменяем импорт
builtins.__import__ = debug_import

print("🐛 ОТЛАДКА ИМПОРТОВ DJANGO")
print("="*50)

BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR))

try:
    # Пробуем настроить Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
    import django
    from django.conf import settings
    
    if not settings.configured:
        settings._setup()
    
    print("🔄 Запуск django.setup()...")
    django.setup()
    print("✅ УСПЕХ! django.setup() выполнен")
    
except Exception as e:
    print(f"\n💥 КРИТИЧЕСКАЯ ОШИБКА: {e}")
    import traceback
    traceback.print_exc()
    
finally:
    # Восстанавливаем оригинальный импорт
    builtins.__import__ = original_import
    
    print(f"\n📊 ИТОГИ:")
    print(f"   Всего импортов: {import_count}")
    print(f"   Проблемные файлы: {problem_files}")