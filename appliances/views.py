from django.shortcuts import render
from django.http import JsonResponse
from appliances.models import ApplianceCategory, ApplianceProduct

def appliance_list(request):
    # Список товаров техники
    products = ApplianceProduct.objects.all()[:50]  # Ограничиваем для производительности
    categories = ApplianceCategory.objects.all()
    
    # Фильтрация по категории
    category_code = request.GET.get('category')
    if category_code:
        products = products.filter(category__code=category_code)
    
    context = {
        'products': products,
        'categories': categories,
        'selected_category': category_code
    }
    return render(request, 'appliances/appliance_list.html', context)

def appliance_detail(request, item_id):
    # Детальная информация о товаре
    try:
        product = ApplianceProduct.objects.get(item_id=item_id)
        context = {'product': product}
        return render(request, 'appliances/appliance_detail.html', context)
    except ApplianceProduct.DoesNotExist:
        return render(request, 'appliances/404.html', status=404)

def category_list(request):
    # Список категорий техники
    categories = ApplianceCategory.objects.all()
    context = {'categories': categories}
    return render(request, 'appliances/category_list.html', context)

def api_stats(request):
    # API для получения статистики
    stats = {
        'categories_count': ApplianceCategory.objects.count(),
        'products_count': ApplianceProduct.objects.count(),
        'products_without_price': ApplianceProduct.objects.filter(price__isnull=True).count(),
    }
    return JsonResponse(stats)
