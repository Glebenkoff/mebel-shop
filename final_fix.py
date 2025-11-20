with open('catalog/views.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Исправляем wishlist_toggle
for i in range(len(lines)):
    if i == 55:  # строка 56 - "AJAX поддержка"
        # Удаляем лишние строки и добавляем правильные
        lines[i+1] = '        if request.headers.get(\'X-Requested-With\') == \'XMLHttpRequest\':\n'
        # Удаляем дублирующую строку 58
        del lines[i+2]
        break

# Исправляем comparison_toggle  
for i in range(len(lines)):
    if i == 93:  # строка 94 - "AJAX поддержка"
        # Заменяем неправильные строки
        lines[i+1] = '        if request.headers.get(\'X-Requested-With\') == \'XMLHttpRequest\':\n'
        # Удаляем строку 95
        del lines[i+2]
        break

with open('catalog/views.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Функции исправлены!")