from django.shortcuts import render, get_object_or_404, redirect
from .utils import get_products_by_category_wrapper as get_products_by_category
from .utils import get_product_content_wrapper as get_product_content
from django.http import JsonResponse
from django.db.models import Q
from .models import Category, PartnerProduct  # Убрали Product, добавили PartnerProduct
import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.utils.text import slugify
from django.views.decorators.csrf import csrf_exempt

def get_all_child_categories(category):
    """Рекурсивно получает все дочерние категории"""
    children = list(category.children.all())
    for child in category.children.all():
        children.extend(get_all_child_categories(child))
    return children

def is_category_in_limited_structure(category, limited_main_category):
    """Проверяет, принадлежит ли категория ограниченной структуре"""
    if category == limited_main_category:
        return True
    
    # Проверяем всех родителей категории
    current = category
    while current.parent:
        if current.parent == limited_main_category:
            return True
        current = current.parent
    
    return False

def catalog_view(request):
    category_slug = request.GET.get('category')
    brand_slugs = request.GET.getlist('brand')
    search_query = request.GET.get('q', '')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    # Находим нашу ограниченную основную категорию
    limited_main_category = Category.objects.filter(
        slug='bytovaya-tekhnika-i-elektronika',
        category_type='main'
    ).first()
    
    if limited_main_category:
        # Получаем все подкатегории основной категории
        all_limited_categories = get_all_child_categories(limited_main_category)
        all_limited_categories.append(limited_main_category)
        
        # Фильтруем товары только по нашим категориям
        products = PartnerProduct.objects.filter(
            category__in=all_limited_categories,
            is_active=True,
            availability=True
        )
    else:
        products = PartnerProduct.objects.filter(is_active=True, availability=True)
    
    # Фильтрация по брендам
    if brand_slugs:
        products = products.filter(producer__in=brand_slugs)
    
    # Поиск
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(part_number__icontains=search_query)
        )
    
    # Фильтрация по цене
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    
    # Пагинация
    paginator = Paginator(products, 20)  # 20 товаров на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Получаем бренды для фильтра
    brands = []
    if limited_main_category:
        brands = limited_main_category.get_brands()
    
    context = {
        'page_obj': page_obj,
        'products': page_obj,
        'brands': brands,
        'search_query': search_query,
        'selected_brands': brand_slugs,
        'min_price': min_price,
        'max_price': max_price,
    }
    
    return render(request, 'catalog/catalog.html', context)

def product_detail(request, product_key):
    """Детальная страница товара"""
    product = get_object_or_404(PartnerProduct, product_key=product_key, is_active=True)
    
    # Получаем похожие товары из той же категории
    similar_products = PartnerProduct.objects.filter(
        category=product.category,
        is_active=True,
        availability=True
    ).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'similar_products': similar_products,
    }
    
    return render(request, 'catalog/product_detail.html', context)

def category_detail(request, category_code):
    """Страница категории"""
    category = get_object_or_404(Category, ocs_category_code=category_code)
    
    products = PartnerProduct.objects.filter(
        category=category,
        is_active=True,
        availability=True
    )
    
    # Пагинация
    paginator = Paginator(products, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
        'products': page_obj,
    }
    
    return render(request, 'catalog/category.html', context)

def catalog_by_category(request, category_code):
    """Каталог по категории OCS"""
    return category_detail(request, category_code)

@csrf_exempt
def add_to_cart(request):
    """Добавление товара в корзину"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            quantity = int(data.get('quantity', 1))
            
            product = get_object_or_404(PartnerProduct, id=product_id, is_active=True)
            
            # Здесь логика добавления в корзину
            # Например, через сессии или модель Cart
            cart = request.session.get('cart', {})
            cart_item = cart.get(str(product_id), {'quantity': 0})
            cart_item['quantity'] += quantity
            cart[str(product_id)] = cart_item
            request.session['cart'] = cart
            request.session.modified = True
            
            return JsonResponse({
                'success': True,
                'message': f'{product.name} добавлен в корзину',
                'cart_count': sum(item['quantity'] for item in cart.values())
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Ошибка: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Неверный метод запроса'})

def get_cart_count(request):
    """Получение количества товаров в корзине"""
    cart = request.session.get('cart', {})
    count = sum(item['quantity'] for item in cart.values())
    return JsonResponse({'count': count})

def debug_ocs(request):
    """Страница отладки OCS API"""
    from .services.ocs_api_service import OCSApiService
    
    api_service = OCSApiService()
    
    # Тестовые данные
    categories = api_service.get_categories()
    test_products = None
    
    # Получаем тестовые товары если есть категории
    if categories:
        # Берем первую категорию для теста
        first_category = categories[0].get('category') if categories else None
        if first_category:
            test_products = api_service.get_products_by_categories([first_category])
    
    context = {
        'categories': categories,
        'test_products': test_products,
        'api_key_set': bool(api_service.api_key),
    }
    
    return render(request, 'debug_ocs.html', context)

# Дополнительные view для обратной совместимости
def catalog_fixed(request):
    """Альтернативный view каталога"""
    return catalog_view(request)

def test_products_fixed(request):
    """Тестовая страница товаров"""
    products = PartnerProduct.objects.filter(is_active=True, availability=True)[:20]
    return render(request, 'catalog/test_products.html', {'products': products})

def catalog_list(request):
    """Простой список товаров"""
    products = PartnerProduct.objects.filter(is_active=True, availability=True)
    return render(request, 'catalog/list.html', {'products': products})