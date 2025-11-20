with open('catalog/views.py', 'r') as f:
    lines = f.readlines()

new_lines = []
i = 0
while i < len(lines):
    if 'def wishlist_toggle' in lines[i] or 'def comparison_toggle' in lines[i]:
        # Пропускаем до конца функции, убирая AJAX блок
        new_lines.append(lines[i])
        i += 1
        while i < len(lines) and 'def ' not in lines[i]:
            if 'XMLHttpRequest' not in lines[i] and 'JsonResponse' not in lines[i]:
                new_lines.append(lines[i])
            i += 1
    else:
        new_lines.append(lines[i])
        i += 1

with open('catalog/views.py', 'w') as f:
    f.writelines(new_lines)

print("AJAX убран из wishlist_toggle и comparison_toggle!")