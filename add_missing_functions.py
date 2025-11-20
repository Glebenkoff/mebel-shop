# add_missing_functions.py
additional_functions = '''

def search_autocomplete(request):
    query = request.GET.get('q', '')
    if len(query) < 2:
        return JsonResponse({'results': []})
    
    products = Product.objects.filter(
        Q(name__icontains=query) | 
        Q(category__name__icontains=query),
        available=True
    )[:8]
    
    results = [{
        'name': product.name,
        'url': product.get_absolute_url(),
        'price': str(product.price),
        'category': product.category.name
    } for product in products]
    
    return JsonResponse({'results': results})

@csrf_exempt
def ajax_wishlist_toggle(request, product_id):
    if request.method == 'POST' and request.user.is_authenticated:
        product = get_object_or_404(Product, id=product_id)
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        
        if product in wishlist.products.all():
            wishlist.products.remove(product)
            message = "Товар удален из избранного"
            added = False
        else:
            wishlist.products.add(product)
            message = "Товар добавлен в избранное"
            added = True
        
        return JsonResponse({
            'success': True,
            'message': message,
            'added': added,
            'wishlist_count': wishlist.products.count()
        })
    
    return JsonResponse({'success': False, 'error': 'Ошибка авторизации'})

@csrf_exempt
def ajax_comparison_toggle(request, product_id):
    if request.method == 'POST' and request.user.is_authenticated:
        product = get_object_or_404(Product, id=product_id)
        comparison, created = Comparison.objects.get_or_create(user=request.user)
        
        if product in comparison.products.all():
            comparison.products.remove(product)
            message = "Товар удален из сравнения"
            added = False
        else:
            comparison.products.add(product)
            message = "Товар добавлен в сравнение"
            added = True
        
        return JsonResponse({
            'success': True,
            'message': message,
            'added': added,
            'comparison_count': comparison.products.count()
        })
    
    return JsonResponse({'success': False, 'error': 'Ошибка авторизации'})
'''

with open('catalog/views.py', 'a', encoding='utf-8') as f:
    f.write(additional_functions)

print("Отсутствующие функции добавлены!")