import os
import re

def fix_all_models():
    print("🔧 АВТОМАТИЧЕСКОЕ ИСПРАВЛЕНИЕ МОДЕЛЕЙ")
    print("=" * 50)
    
    # Список приложений для проверки
    apps = ['catalog', 'accounts', 'cart', 'main', 'pages']
    
    for app in apps:
        models_file = os.path.join(app, 'models.py')
        print(f"\n📁 Обрабатываем {app}...")
        
        if not os.path.exists(models_file):
            print(f"  ⚠️  Файл не найден, пропускаем")
            continue
            
        try:
            # Читаем файл
            with open(models_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Создаем backup
            backup_file = models_file + '.backup'
            with open(backup_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Исправляем index_together
            original_content = content
            content = re.sub(
                r'index_together\s*=\s*\[[^\]]*\]', 
                '# index_together removed - compatible with newer Django', 
                content
            )
            
            # Если ничего не изменилось, но есть упоминание index_together
            if content == original_content and 'index_together' in content:
                content = content.replace('index_together', '# OBSOLETE: index_together')
            
            # Записываем исправленную версию
            with open(models_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"  ✅ Файл исправлен")
            
        except Exception as e:
            print(f"  ❌ Ошибка: {e}")

if __name__ == '__main__':
    fix_all_models()
    print("\n🎉 ВСЕ ФАЙЛЫ ОБРАБОТАНЫ!")
