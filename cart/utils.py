from .models import Cart

def get_cart(request):
    cart_id = request.session.get('cart_id')
    if cart_id:
        try:
            return Cart.objects.get(id=cart_id)
        except Cart.DoesNotExist:
            pass
    
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        cart = Cart.objects.create()
    
    request.session['cart_id'] = cart.id
    return cart
