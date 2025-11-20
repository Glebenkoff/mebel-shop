import sqlite3
from pathlib import Path

db_path = Path("db.sqlite3")
if db_path.exists():
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    
    print("📊 СОЗДАННЫЕ ТАБЛИЦЫ:")
    print("=" * 30)
    
    for table in sorted(tables):
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"  ✅ {table}: {count} записей")
    
    conn.close()
    
    # Проверяем основные таблицы
    essential_tables = ['django_migrations', 'auth_user', 'catalog_category', 'catalog_product']
    missing = [t for t in essential_tables if t not in tables]
    
    if missing:
        print(f"\n❌ Отсутствуют таблицы: {missing}")
    else:
        print(f"\n🎉 Все основные таблицы созданы!")
else:
    print("❌ База данных не найдена")
