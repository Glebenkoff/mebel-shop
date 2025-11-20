# fix_indentation.py
with open('catalog/views.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Исправляем отступы
fixed_lines = []
for line in lines:
    if "'success': True," in line and not line.startswith(' ' * 16):
        fixed_lines.append(' ' * 16 + line.lstrip())
    else:
        fixed_lines.append(line)

with open('catalog/views.py', 'w', encoding='utf-8') as f:
    f.writelines(fixed_lines)

print("Отступы исправлены!")