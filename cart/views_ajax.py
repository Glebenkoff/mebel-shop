from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Cart

@login_required
def cart_count_ajax(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return JsonResponse({'count': cart.get_total_quantity()})