# clean_fix.py
with open('catalog/views.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Найдем функцию wishlist_toggle и исправим ее
in_wishlist = False
fixed_lines = []
i = 0

while i < len(lines):
    line = lines[i]
    
    if 'def wishlist_toggle' in line:
        in_wishlist = True
        fixed_lines.append(line)
        i += 1
        # Копируем функцию до блока AJAX
        while i < len(lines) and 'added = True' not in lines[i]:
            fixed_lines.append(lines[i])
            i += 1
        
        # Добавляем строку после added = True
        fixed_lines.append(lines[i])  # added = True
        i += 1
        
        # Добавляем правильный AJAX блок
        ajax_block = [
            '\n',
            '        # AJAX поддержка\n',
            '        if request.headers.get(\'X-Requested-With\') == \'XMLHttpRequest\':\n',
            '            return JsonResponse({\n',
            '                \'success\': True,\n',
            '                \'message\': message,\n',
            '                \'added\': added,\n',
            '                \'wishlist_count\': wishlist.products.count()\n',
            '            })\n',
            '\n'
        ]
        fixed_lines.extend(ajax_block)
        
        # Пропускаем испорченный код до return redirect
        while i < len(lines) and 'return redirect' not in lines[i]:
            i += 1
        
        # Добавляем return redirect
        if i < len(lines):
            fixed_lines.append(lines[i])
            i += 1
            
    else:
        fixed_lines.append(line)
        i += 1

with open('catalog/views.py', 'w', encoding='utf-8') as f:
    f.writelines(fixed_lines)

print("Функция wishlist_toggle исправлена!")