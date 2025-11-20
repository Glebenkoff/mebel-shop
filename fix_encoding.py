# fix_encoding.py
with open('catalog/views.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    if 'def wishlist_toggle' in line or 'def comparison_toggle' in line:
        # Добавляем заголовок функции
        new_lines.append(line)
        i += 1
        # Пропускаем AJAX блок
        while i < len(lines) and not lines[i].startswith('def '):
            if 'XMLHttpRequest' not in lines[i] and 'JsonResponse' not in lines[i]:
                new_lines.append(lines[i])
            i += 1
    else:
        new_lines.append(line)
        i += 1

with open('catalog/views.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Готово! AJAX удален.")