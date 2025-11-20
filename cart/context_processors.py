from .models import Cart

def cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        return {
            'cart': cart,
            'cart_item_count': cart.get_total_quantity()
        }
    return {'cart': None, 'cart_item_count': 0}