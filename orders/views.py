from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .forms import OrderCreateForm
from .models import Cart, CartItem, Order, OrderItem
from cart.context_processors import cart_count
from catalog.models import PartnerProduct
from django.db.models import F
import uuid

def _get_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_id = request.session.get('cart_session_id')
        if not session_id:
            session_id = str(uuid.uuid4())
            request.session['cart_session_id'] = session_id
        cart, created = Cart.objects.get_or_create(session_id=session_id)
    return cart

def add_to_cart(request, product_id):
    product = get_object_or_404(PartnerProduct, id=product_id)
    cart = _get_cart(request)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f"{product.name} добавлен в корзину!")
    return redirect("cart_detail")

def cart_detail(request):
    cart = _get_cart(request)
    items = cart.items.all().select_related('product')
    # Используем base_price вместо price
    total = sum(item.product.price * item.quantity for item in items)
    return render(request, "orders/cart.html", {"cart": cart, "items": items, "total": total})

@require_POST
@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    messages.success(request, "Товар удалён из корзины.")
    return JsonResponse({'success': True})  # или redirect, но не оба сразу

def update_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        if 1 <= quantity <= 99:
            item.quantity = quantity
            item.save()
            messages.success(request, "Количество обновлено.")
        else:
            messages.error(request, "Некорректное количество.")
    return redirect("cart_detail")

@login_required
def create_order(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "Ваша корзина пуста.")
        return redirect('cart:cart_detail')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = 0
            order.save()

            total = 0
            for product_key, item in cart.items():
                OrderItem.objects.create(
                    order=order,
                    product_key=product_key,
                    name=item['name'],
                    price=item['price'],
                    quantity=item['quantity']
                )
                total += item['price'] * item['quantity']

            order.total_price = total
            order.save()

            # Очистить корзину
            request.session['cart'] = {}
            request.session.modified = True

            messages.success(request, f"Заказ #{order.id} успешно оформлен!")
            return redirect('orders:order_detail', pk=order.id)  # ← Вот эта строка должна быть на своём уровне
    else:
        form = OrderCreateForm()

    return render(request, 'orders/create.html', {'form': form})    

def order_success(request):
    return render(request, "orders/order_success.html")

def home(request):
    return render(request, 'home.html')

def order_detail(request, pk):
    order = get_object_or_404(Order, id=pk, user=request.user)
    return render(request, 'orders/detail.html', {'order': order})