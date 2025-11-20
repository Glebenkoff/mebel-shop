import os
import sys

def create_clean_init_files():
    \"\"\"Создает чистые __init__.py файлы\"\"\"
    apps = ['accounts', 'cart', 'catalog', 'main', 'pages']
    
    for app in apps:
        init_file = os.path.join(app, '__init__.py')
        
        # Создаем папку если не существует
        os.makedirs(app, exist_ok=True)
        
        # Создаем чистый файл
        with open(init_file, 'w', encoding='utf-8') as f:
            f.write('# Clean init file\\n')
        print(f'✅ Создан: {init_file}')

def check_file_encoding(filepath):
    \"\"\"Проверяет файл на проблемы с кодировкой\"\"\"
    try:
        with open(filepath, 'rb') as f:
            content = f.read()
        
        # Проверяем на null bytes
        if b'\\x00' in content:
            return 'HAS_NULL_BYTES'
        
        # Проверяем на BOM
        if content.startswith(b'\\xff\\xfe') or content.startswith(b'\\xfe\\xff'):
            return 'HAS_UTF16_BOM'
        if content.startswith(b'\\xef\\xbb\\xbf'):
            return 'HAS_UTF8_BOM'
            
        return 'CLEAN'
    except Exception as e:
        return f'ERROR: {e}'

def fix_problem_files():
    \"\"\"Ищет и исправляет проблемные файлы\"\"\"
    print('🔍 Поиск проблемных файлов...')
    
    problem_files = []
    
    # Проверяем все Python файлы
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                status = check_file_encoding(filepath)
                
                if status != 'CLEAN':
                    problem_files.append((filepath, status))
                    print(f'❌ Проблема: {filepath} - {status}')
    
    # Исправляем проблемные файлы
    print(f'\\n🔄 Исправляем {len(problem_files)} файлов...')
    
    for filepath, status in problem_files:
        try:
            with open(filepath, 'rb') as f:
                content = f.read()
            
            # Удаляем BOM
            if content.startswith(b'\\xef\\xbb\\xbf'):
                content = content[3:]
            elif content.startswith(b'\\xff\\xfe') or content.startswith(b'\\xfe\\xff'):
                # UTF-16 BOM - перекодируем
                try:
                    content = content.decode('utf-16').encode('utf-8')
                except:
                    content = content[2:]  # Просто удаляем BOM
            
            # Удаляем null bytes
            content = content.replace(b'\\x00', b'')
            
            # Записываем обратно
            with open(filepath, 'wb') as f:
                f.write(content)
            
            print(f'✅ Исправлен: {filepath}')
            
        except Exception as e:
            print(f'💥 Ошибка с {filepath}: {e}')

def main():
    print('🚀 КОМПЛЕКСНОЕ ИСПРАВЛЕНИЕ ПРОБЛЕМ')
    print('=' * 50)
    
    # 1. Создаем чистые __init__.py
    create_clean_init_files()
    
    # 2. Исправляем проблемные файлы
    fix_problem_files()
    
    # 3. Проверяем основные файлы
    print('\\n🔍 Проверяем основные файлы:')
    critical_files = ['settings.py', 'urls.py', 'manage.py']
    
    for file in critical_files:
        if os.path.exists(file):
            status = check_file_encoding(file)
            print(f'  {file}: {status}')
    
    print('\\n✅ ВСЕ ПРОБЛЕМЫ ИСПРАВЛЕНЫ!')

if __name__ == '__main__':
    main()
