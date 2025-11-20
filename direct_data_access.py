"""
ПРЯМОЙ ДОСТУП К ДАННЫМ - обход проблем Django
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime

def get_database_stats():
    """Получение статистики напрямую из базы"""
    db_path = Path(__file__).parent / 'db.sqlite3'
    
    print(f"🔍 Проверяем базу данных: {db_path}")
    
    if not db_path.exists():
        print("❌ База данных не найдена!")
        return {"error": "База данных не найдена"}
    
    stats = {}
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Получаем список таблиц
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [table[0] for table in cursor.fetchall()]
        
        print("📊 СТАТИСТИКА БАЗЫ ДАННЫХ")
        print("="*40)
        print(f"Найдено таблиц: {len(tables)}")
        
        for table in tables:
            if not table.startswith('sqlite_'):
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table};")
                    count = cursor.fetchone()[0]
                    stats[table] = count
                    print(f"   ✅ {table}: {count} записей")
                except Exception as e:
                    print(f"   ❌ {table}: ошибка - {e}")
                    stats[table] = f"ошибка: {e}"
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Ошибка подключения к базе: {e}")
        stats["error"] = str(e)
    
    return stats

def main():
    """Основная функция"""
    print("🚀 ПРЯМОЙ ДОСТУП К ДАННЫМ")
    print("📍 Обход проблем Django")
    print("="*50)
    
    # Получаем статистику
    stats = get_database_stats()
    
    print(f"\n📈 ИТОГИ:")
    for table, count in stats.items():
        if table != "error":
            print(f"   {table}: {count}")
    
    print("\n✅ ВЫПОЛНЕНИЕ ЗАВЕРШЕНО")

if __name__ == "__main__":
    main()