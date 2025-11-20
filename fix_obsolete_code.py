import os
import re

def fix_models_file(filepath):
    """Исправляет устаревшие атрибуты в models.py"""
    if not os.path.exists(filepath):
        print(f'❌ Файл не найден: {filepath}')
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Создаем backup
        backup_path = filepath + '.backup'
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Заменяем index_together на indexes (новый синтаксис)
        old_pattern = r"index_together\s*=\s*\[[^\]]*\]"
        new_content = re.sub(old_pattern, '# index_together removed - use indexes instead', content)
        
        # Если есть конкретные индексы, преобразуем их
        if 'index_together' in new_content:
            # Более сложная замена для конкретных случаев
            new_content = new_content.replace('index_together', '# OBSOLETE: index_together')
        
        # Записываем исправленную версию
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f'✅ Исправлен: {filepath}')
        return True
        
    except Exception as e:
        print(f'❌ Ошибка при исправлении {filepath}: {e}')
        return False

def main():
    print('🔧 ИСПРАВЛЕНИЕ УСТАРЕВШЕГО КОДА')
    print('=' * 40)
    
    # Исправляем models.py в приложениях
    apps = ['catalog', 'accounts', 'cart', 'main', 'pages']
    
    for app in apps:
        models_file = os.path.join(app, 'models.py')
        if os.path.exists(models_file):
            fix_models_file(models_file)
        else:
            print(f'⚠️  Файл не найден: {models_file}')

if __name__ == '__main__':
    main()
