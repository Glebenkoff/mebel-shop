# fix_cart_redirects.py
with open('cart/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Заменяем все неправильные редиректы
new_content = content.replace("redirect('cart:cart_detail')", "redirect('cart_detail')")
new_content = new_content.replace('redirect("cart:cart_detail")', 'redirect("cart_detail")')

with open('cart/views.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Редиректы в cart/views.py исправлены!")