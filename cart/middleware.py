from .models import Cart

class CartMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
            request.cart_item_count = cart.get_total_quantity()
        else:
            request.cart_item_count = 0
        
        response = self.get_response(request)
        return response