# fix_json_response.py
with open('catalog/views.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Найдем строку 56 и добавим недостающую строку
for i in range(len(lines)):
    if i == 55 and 'AJAX поддержка' in lines[i]:  # строка 56
        # Добавляем недостающую строку return JsonResponse({
        lines.insert(i + 1, '            return JsonResponse({\n')
        break

with open('catalog/views.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Недостающая строка добавлена!")