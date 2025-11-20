import os
import django
import sys

print('🧪 ТЕСТИРУЕМ DJANGO')
print('=' * 40)

try:
    # Настраиваем Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
    django.setup()
    print('✅ Django setup - УСПЕХ!')
    
    # Проверяем основные компоненты
    from django.conf import settings
    print(f'✅ Settings: DEBUG={settings.DEBUG}')
    
    from django.contrib.auth import get_user_model
    User = get_user_model()
    print('✅ Auth system - OK')
    
    # Проверяем базу данных
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute('SELECT COUNT(*) FROM auth_user')
        count = cursor.fetchone()[0]
        print(f'✅ Database: {count} пользователей')
    
    print('\\n🎉 ВСЕ СИСТЕМЫ РАБОТАЮТ!')
    
except Exception as e:
    print(f'❌ Ошибка: {e}')
    print(f'Тип ошибки: {type(e).__name__}')
    
    # Детальная диагностика
    import traceback
    print('\\n�� Детали ошибки:')
    traceback.print_exc()
