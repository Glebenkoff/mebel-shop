# remove_duplicate_handler.py
with open('templates/catalog/product_list.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Удаляем дублирующий JavaScript обработчик
import re

# Находим и удаляем весь блок AJAX добавления в корзину
pattern = r'// AJAX добавление в корзину[\s\S]*?\.then\(data => \{[\s\S]*?// Обновляем счетчик в шапке'
new_content = re.sub(pattern, '', content)

with open('templates/catalog/product_list.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Дублирующий обработчик удален!")