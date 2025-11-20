# fix_annotation.py
with open('catalog/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Исправляем проблему с аннотацией - убираем лишние символы
content = content.replace("'success': True,", "                'success': True,")
content = content.replace("'message': message,", "                'message': message,")
content = content.replace("'added': added,", "                'added': added,")
content = content.replace("'wishlist_count': wishlist.products.count()", "                'wishlist_count': wishlist.products.count()")
content = content.replace("'comparison_count': comparison.products.count()", "                'comparison_count': comparison.products.count()")

with open('catalog/views.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Аннотации исправлены!")