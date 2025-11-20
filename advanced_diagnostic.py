import os
import sys
import django
from pathlib import Path

print('🔍 ДИАГНОСТИКА СИСТЕМЫ')
print('=' * 50)

# 1. Проверяем базовые импорты
print('1. Базовые импорты Python...')
try:
    import sqlite3
    print('   ✅ sqlite3 - OK')
except ImportError as e:
    print(f'   ❌ sqlite3 - ERROR: {e}')

# 2. Проверяем Django
print('2. Проверка Django...')
try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
    django.setup()
    print('   ✅ Django setup - OK')
    
    # Проверяем основные модули
    from django.conf import settings
    print(f'   ✅ Django settings - OK (DEBUG={settings.DEBUG})')
    
    from django.contrib.auth import get_user_model
    print('   ✅ Django auth - OK')
    
except Exception as e:
    print(f'   ❌ Django setup - ERROR: {e}')

# 3. Проверяем базу данных
print('3. Проверка базы данных...')
db_path = Path('db.sqlite3')
if db_path.exists():
    print(f'   ✅ DB exists: {db_path}')
    
    import sqlite3
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Получаем список таблиц
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f'   ✅ Tables count: {len(tables)}')
        
        # Проверяем основные таблицы
        essential_tables = ['catalog_product', 'catalog_category', 'auth_user']
        for table in essential_tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f'   ✅ {table}: {count} записей')
            except:
                print(f'   ⚠️  {table}: не найдена')
        
        conn.close()
    except Exception as e:
        print(f'   ❌ DB connection error: {e}')
else:
    print('   ❌ DB file not found')

print('=' * 50)
print('📊 ДИАГНОСТИКА ЗАВЕРШЕНА')
