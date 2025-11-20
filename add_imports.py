# add_imports.py
with open('catalog/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Добавляем недостающие импорты в начало файла
if 'from django.views.decorators.csrf import csrf_exempt' not in content:
    content = content.replace(
        'from django.http import JsonResponse',
        'from django.http import JsonResponse\nfrom django.views.decorators.csrf import csrf_exempt'
    )

with open('catalog/views.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Импорты добавлены!")