# fix_both_functions.py
with open('catalog/views.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Исправляем обе функции
fixed_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    
    # Для wishlist_toggle
    if 'def wishlist_toggle' in line:
        fixed_lines.append(line)
        i += 1
        while i < len(lines) and 'return redirect' not in lines[i]:
            if 'AJAX поддержка' in lines[i]:
                fixed_lines.append(lines[i])  # AJAX поддержка
                i += 1
                fixed_lines.append(lines[i])  # if request.headers...
                i += 1
                fixed_lines.append('            return JsonResponse({\n')  # Добавляем недостающую строку
            else:
                fixed_lines.append(lines[i])
                i += 1
        fixed_lines.append(lines[i])  # return redirect
        i += 1
    
    # Для comparison_toggle  
    elif 'def comparison_toggle' in line:
        fixed_lines.append(line)
        i += 1
        while i < len(lines) and 'return redirect' not in lines[i]:
            if 'AJAX поддержка' in lines[i]:
                fixed_lines.append(lines[i])  # AJAX поддержка
                i += 1
                fixed_lines.append(lines[i])  # if request.headers...
                i += 1
                fixed_lines.append('            return JsonResponse({\n')  # Добавляем недостающую строку
            else:
                fixed_lines.append(lines[i])
                i += 1
        fixed_lines.append(lines[i])  # return redirect
        i += 1
    
    else:
        fixed_lines.append(line)
        i += 1

with open('catalog/views.py', 'w', encoding='utf-8') as f:
    f.writelines(fixed_lines)

print("Обе функции исправлены!")