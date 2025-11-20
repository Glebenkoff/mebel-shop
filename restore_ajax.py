# restore_ajax.py
with open('catalog/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Восстанавливаем оригинальные функции
original_wishlist = '''@login_required
def wishlist_toggle(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.user.is_authenticated:
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        
        if product in wishlist.products.all():
            wishlist.products.remove(product)
            message = "Товар удален из избранного"
            added = False
        else:
            wishlist.products.add(product)
            message = "Товар добавлен в избранное"
            added = True
        
        # AJAX поддержка
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': message,
                'added': added,
                'wishlist_count': wishlist.products.count()
            })
    
    # Обычный редирект
    return redirect('catalog:wishlist')'''

content = content.replace('''@login_required
def wishlist_toggle(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.user.is_authenticated:
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        
        if product in wishlist.products.all():
            wishlist.products.remove(product)
            messages.success(request, "Товар удален из избранного")
        else:
            wishlist.products.add(product)
            messages.success(request, "Товар добавлен в избранное")
    
    # ВСЕГДА редирект - убрали AJAX проверку
    return redirect('catalog:wishlist')''', original_wishlist)

with open('catalog/views.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("AJAX восстановлен!")