from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from catalog.models import Product
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart/cart_detail.html', {'cart': cart})

@login_required
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart.objects.filter(user=request.user).first()
    if not cart:
        cart = Cart.objects.create(user=request.user)
    
    # Используем get_or_create, но с проверкой существования
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, 
        product=product,
        defaults={'quantity': 1}
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f'Товар "{product.name}" добавлен в корзину!')
    return redirect(request.META.get('HTTP_REFERER', 'product_list'))

@login_required
def cart_remove(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart.objects.filter(user=request.user).first()
    
    if cart:
        # Используем filter().first() вместо get() для безопасности
        cart_item = CartItem.objects.filter(cart=cart, product=product).first()
        if cart_item:
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
    
    return redirect('cart_detail')

@csrf_exempt
def cart_add_ajax(request, product_id):
    """AJAX добавление в корзину"""
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Требуется авторизация'})
    
    try:
        product = Product.objects.get(id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Товар "{product.name}" добавлен в корзину',
            'cart_count': cart.get_total_quantity(),
            'cart_total': cart.get_total_price()
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})