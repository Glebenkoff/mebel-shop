from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Cart, CartItem
from catalog.models import Product
from django.http import JsonResponse

def cart_detail(request):
    cart = Cart.objects.first()  # Временно - потом добавим логику сессий
    return render(request, 'cart/cart_detail.html', {'cart': cart})

def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(id=1)  # Временно
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, 
        product=product
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f'Товар "{product.name}" добавлен в корзину!')
    return redirect('product_list')

def cart_remove(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart.objects.first()  # Временно
    
    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.delete()
        messages.success(request, f'Товар "{product.name}" удален из корзины!')
    except CartItem.DoesNotExist:
        messages.error(request, 'Товар не найден в корзине')
    
    return redirect('cart_detail')