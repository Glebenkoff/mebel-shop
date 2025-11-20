#!/usr/bin/env python
"""
СКРИПТ ДЛЯ ПОИСКА ПРОБЛЕМНОГО ФАЙЛА
"""

import os
import sys
from pathlib import Path

print("🔍 ПОИСК ПРОБЛЕМНОГО ФАЙЛА")
print("="*50)

BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR))

# Используем минимальные настройки
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'minimal_settings')

try:
    import django
    from django.conf import settings
    
    # Принудительная настройка с минимальными настройками
    if not settings.configured:
        import minimal_settings
        settings.configure(**{k: v for k, v in minimal_settings.__dict__.items() if not k.startswith('_')})
    
    print("✅ Минимальные настройки загружены")
    
    # Теперь пробуем django.setup()
    print("🔄 Запуск django.setup()...")
    django.setup()
    print("✅ django.setup() выполнен успешно!")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
    print("\n🔧 ДИАГНОСТИКА:")
    
    # Пробуем определить какой модуль вызывает проблему
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    
    for frame in tb:
        if 'import' in frame.line or 'from' in frame.line:
            print(f"   Файл: {frame.filename}")
            print(f"   Строка: {frame.line}")
            print(f"   Модуль: {frame.name}")
            print("   ---")