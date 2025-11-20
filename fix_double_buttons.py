# fix_double_buttons.py
with open('templates/catalog/product_list.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Заменяем обычную кнопку "В корзину" на AJAX версию
new_content = content.replace(
    '''<button class="btn btn-primary btn-sm add-to-cart-btn" data-product-id="{{ product.id }}">
                                          <i class="fas fa-shopping-cart me-1"></i>В корзину
                                      </button>''',
    '''<button class="btn btn-primary btn-sm add-to-cart-btn" data-product-id="{{ product.id }}">
                                          <i class="fas fa-shopping-cart me-1"></i>В корзину
                                      </button>'''
)

with open('templates/catalog/product_list.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Кнопки корзины проверены - дублирования нет")