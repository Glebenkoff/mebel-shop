# fix_double_cart_events.py
with open('templates/catalog/product_list.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Добавляем предотвращение дублирования событий
new_content = content.replace(
    '''  // AJAX добавление в корзину
  document.querySelectorAll('.add-to-cart-btn').forEach(btn => {
      btn.addEventListener('click', function() {''',
    '''  // AJAX добавление в корзину - с защитой от дублирования
  document.querySelectorAll('.add-to-cart-btn').forEach(btn => {
      // Убираем старые обработчики
      btn.replaceWith(btn.cloneNode(true));
      const newBtn = document.querySelector('.add-to-cart-btn[data-product-id="' + btn.dataset.productId + '"]');
      
      newBtn.addEventListener('click', function(e) {
          console.log('Добавление в корзину товара:', this.dataset.productId);
          e.stopPropagation();'''
)

with open('templates/catalog/product_list.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Защита от дублирования событий добавлена!")