import os
import re

def check_obsolete_code(filepath):
    """Проверяет файл на устаревшие атрибуты Django"""
    if not os.path.exists(filepath):
        return []
    
    obsolete_patterns = [
        (r'index_together', 'index_together (заменен на indexes)'),
        (r'class META:', 'class META: (должен быть class Meta:)'),
        (r'on_delete=None', 'on_delete=None (должен быть указан on_delete)'),
    ]
    
    found_issues = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            for pattern, description in obsolete_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    found_issues.append(f'Строка {i}: {description}')
    
    except Exception as e:
        found_issues.append(f'Ошибка чтения: {e}')
    
    return found_issues

def main():
    print('🔍 ПРОВЕРКА НА УСТАРЕВШИЙ КОД')
    print('=' * 50)
    
    apps = ['catalog', 'accounts', 'cart', 'main', 'pages']
    
    for app in apps:
        models_file = os.path.join(app, 'models.py')
        print(f'\n📁 {app}:')
        
        if os.path.exists(models_file):
            issues = check_obsolete_code(models_file)
            if issues:
                for issue in issues:
                    print(f'  ❌ {issue}')
            else:
                print(f'  ✅ Нет устаревшего кода')
        else:
            print(f'  ⚠️  Файл не найден')

if __name__ == '__main__':
    main()
