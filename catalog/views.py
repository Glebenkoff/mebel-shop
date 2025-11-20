from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Product, Category, Wishlist, Comparison
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def product_list(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(available=True)
    
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(category__name__icontains=query)
        )
    
    return render(request, 'catalog/product_list.html', {
        'products': products,
        'query': query
    })

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug)
    return render(request, 'catalog/product_detail.html', {'product': product})

def product_search(request):
    return product_list(request)

@login_required
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
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': message,
                'added': added,
                'wishlist_count': wishlist.products.count()
            })
    
    return redirect('catalog:wishlist')

@login_required
def wishlist_view(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    products = wishlist.products.all()
    
    return render(request, 'catalog/wishlist.html', {
        'wishlist': wishlist,
        'products': products
    })

@login_required
def comparison_toggle(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.user.is_authenticated:
        comparison, created = Comparison.objects.get_or_create(user=request.user)
        
        if product in comparison.products.all():
            comparison.products.remove(product)
            message = "Товар удален из сравнения"
            added = False
        else:
            comparison.products.add(product)
            message = "Товар добавлен в сравнение"
            added = True
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': message,
                'added': added,
                'comparison_count': comparison.products.count()
            })
    
    return redirect('catalog:comparison')

@login_required
def comparison_view(request):
    comparison, created = Comparison.objects.get_or_create(user=request.user)
    products = comparison.products.all()
    
    return render(request, 'catalog/comparison.html', {
        'comparison': comparison,
        'products': products
    })


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
