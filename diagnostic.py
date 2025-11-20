#!/usr/bin/env python
"""
ДИАГНОСТИЧЕСКИЙ СКРИПТ - проверка структуры проекта
"""

import os
import sys
from pathlib import Path

def diagnose_project():
    """Диагностика структуры проекта"""
    
    current_dir = Path(__file__).parent
    print("🔍 ДИАГНОСТИКА СТРУКТУРЫ ПРОЕКТА")
    print(f"📍 Текущая папка: {current_dir}")
    print("="*50)
    
    # Проверяем основные папки
    folders_to_check = [
        'mebel_shop',
        'catalog', 
        'cart',
        'accounts',
        'venv'
    ]
    
    print("📂 ПРОВЕРКА ПАПОК:")
    for folder in folders_to_check:
        folder_path = current_dir / folder
        if folder_path.exists():
            print(f"   ✅ {folder}: существует")
            # Покажем что внутри
            if folder in ['mebel_shop', 'catalog']:
                items = list(folder_path.glob("*.py"))
                print(f"      Файлы: {[f.name for f in items]}")
        else:
            print(f"   ❌ {folder}: не найдена")
    
    print("\n🔧 ПРОВЕРКА НАСТРОЕК DJANGO:")
    settings_file = current_dir / 'mebel_shop' / 'settings.py'
    if settings_file.exists():
        print(f"   ✅ settings.py: найден")
        
        # Читаем первые 10 строк settings.py
        with open(settings_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()[:10]
            print("   📋 Содержимое (первые 10 строк):")
            for line in lines:
                print(f"      {line.strip()}")
    else:
        print(f"   ❌ settings.py: не найден")
    
    print("\n🐍 ПРОВЕРКА PYTHON PATH:")
    print(f"   Python path: {sys.path}")

if __name__ == "__main__":
    diagnose_project()