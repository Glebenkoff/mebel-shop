import os
import glob

def clean_file(filepath):
    """Очищает файл от null bytes"""
    try:
        with open(filepath, 'rb') as f:
            content = f.read()
        
        # Проверяем на наличие null bytes
        if b'\x00' in content:
            print(f'🧹 Очищаем файл: {filepath}')
            
            # Удаляем null bytes
            clean_content = content.replace(b'\x00', b'')
            
            # Создаем backup
            backup_path = filepath + '.backup'
            with open(backup_path, 'wb') as f:
                f.write(content)
            
            # Записываем очищенный контент
            with open(filepath, 'wb') as f:
                f.write(clean_content)
            
            return True
        return False
    except Exception as e:
        print(f'❌ Ошибка при обработке {filepath}: {e}')
        return False

def main():
    print('🔍 Поиск файлов с null bytes...')
    
    # Ищем все Python файлы
    python_files = glob.glob('**/*.py', recursive=True)
    cleaned_count = 0
    
    for filepath in python_files:
        if clean_file(filepath):
            cleaned_count += 1
    
    print(f'✅ Очищено файлов: {cleaned_count}')
    
    # Проверяем основные файлы
    critical_files = ['settings.py', 'urls.py', 'manage.py']
    print('\n🔍 Проверяем критические файлы:')
    
    for file in critical_files:
        if os.path.exists(file):
            with open(file, 'rb') as f:
                content = f.read()
                has_null = b'\x00' in content
                status = '❌ ЕСТЬ NULL BYTES' if has_null else '✅ ЧИСТЫЙ'
                print(f'  {file}: {status}')

if __name__ == '__main__':
    main()
