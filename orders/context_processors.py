# orders/context_processors.py
from .views import _get_cart

def cart_count(request):
    cart = request.session.get('cart', {})
    if isinstance(cart, dict):
        total = sum(item.get('quantity', 0) for item in cart.values())
    else:
        total = 0
    return {'cart_count': total}