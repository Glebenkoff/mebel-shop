# fix_ajax_removal.py
import os

# Проверим шаблоны избранного и сравнения
templates_to_check = [
    'catalog/templates/catalog/wishlist.html',
    'catalog/templates/catalog/comparison.html'
]

for template_path in templates_to_check:
    if os.path.exists(template_path):
        print(f"=== Проверяем {template_path} ===")
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Ищем кнопки удаления
            if 'remove' in content.lower() or 'delete' in content.lower() or 'toggle' in content.lower():
                print("Найдены кнопки удаления")
                
                # Покажем контекст
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if 'remove' in line.lower() or 'delete' in line.lower() or 'toggle' in line.lower():
                        print(f"Строка {i+1}: {line.strip()}")
            
            # Проверим есть ли JavaScript для обновления DOM
            if 'script' in content:
                print("Найден JavaScript в шаблоне")
            else:
                print("⚠️ В шаблоне НЕТ JavaScript для обновления DOM после AJAX")

print("\n=== РЕКОМЕНДАЦИЯ ===")
print("Нужно добавить JavaScript в шаблоны wishlist.html и comparison.html")
print("который будет удалять товар из DOM после успешного AJAX запроса")