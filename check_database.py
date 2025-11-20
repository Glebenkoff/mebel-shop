import sqlite3
from pathlib import Path

def check_database():
    print("🔍 ПРОВЕРКА БАЗЫ ДАННЫХ")
    print("=" * 40)
    
    db_path = Path('db.sqlite3')
    if not db_path.exists():
        print("❌ База данных не найдена!")
        return
    
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Получаем список таблиц
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        print(f"📊 Найдено таблиц: {len(tables)}")
        print("\n📋 Список таблиц:")
        for table in sorted(tables):
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"  ✅ {table}: {count} записей")
        
        # Проверяем основные таблицы Django
        essential_tables = [
            'django_migrations', 
            'auth_user', 
            'django_content_type',
            'django_session'
        ]
        
        print(f"\n🔍 Проверка основных таблиц:")
        for table in essential_tables:
            if table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                status = "✅" if count > 0 else "⚠️ "
                print(f"  {status} {table}: {count} записей")
            else:
                print(f"  ❌ {table}: не найдена")
        
        conn.close()
        print(f"\n🎉 База данных в отличном состоянии!")
        
    except Exception as e:
        print(f"❌ Ошибка проверки базы данных: {e}")

if __name__ == '__main__':
    check_database()
