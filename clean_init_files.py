import os
import glob

def clean_init_files():
    print('🧹 Очищаем все __init__.py файлы...')
    
    # Находим все __init__.py файлы
    init_files = glob.glob('**/__init__.py', recursive=True)
    
    for filepath in init_files:
        print(f'Обрабатываем: {filepath}')
        
        try:
            # Читаем файл в бинарном режиме
            with open(filepath, 'rb') as f:
                content = f.read()
            
            # Удаляем BOM (EF BB BF) и null bytes
            if content.startswith(b'\xef\xbb\xbf'):
                content = content[3:]  # Удаляем UTF-8 BOM
            content = content.replace(b'\x00', b'')  # Удаляем null bytes
            
            # Если файл не пустой и не содержит только BOM, сохраняем очищенный контент
            if content.strip():
                # Создаем backup
                backup_path = filepath + '.backup'
                with open(backup_path, 'wb') as f:
                    f.write(content)
                
                # Записываем очищенную версию
                with open(filepath, 'wb') as f:
                    f.write(content)
                print(f'  ✅ Очищен: {filepath}')
            else:
                # Если файл пустой после очистки, создаем пустой файл
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write('')
                print(f'  ✅ Создан пустой: {filepath}')
                
        except Exception as e:
            print(f'  ❌ Ошибка с {filepath}: {e}')
            
            # Если не удалось очистить, создаем новый пустой файл
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write('')
                print(f'  ✅ Пересоздан: {filepath}')
            except:
                print(f'  💥 Не удалось восстановить: {filepath}')

if __name__ == '__main__':
    clean_init_files()
    print('✅ Все __init__.py файлы очищены!')
