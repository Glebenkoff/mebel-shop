from django.shortcuts import render, get_object_or_404, redirect
from .utils import get_products_by_category_wrapper as get_products_by_category
from .utils import get_product_content_wrapper as get_product_content
from django.http import JsonResponse
from django.db.models import Q
from .models import Product, Category, PartnerProduct
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
            category__in=all_limited_categories
        )
    else:
        # Если ограниченная категория не найдена, показываем пустой список
        products = PartnerProduct.objects.none()

    current_category = None
    current_brand = None

    # Поиск по названию
    if search_query:
        products = products.filter(name__icontains=search_query)

    # Фильтрация по цене
    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
        except (ValueError, TypeError):
            pass

    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except (ValueError, TypeError):
            pass

    # Фильтрация по категории (в пределах ограниченных категорий)
    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        
        # Проверяем, что категория принадлежит нашей ограниченной структуре
        if limited_main_category and is_category_in_limited_structure(current_category, limited_main_category):
            all_categories = get_all_child_categories(current_category)
            all_categories.append(current_category)
            products = products.filter(category__in=all_categories)
        else:
            # Если категория не из нашей структуры, показываем пустой список
            products = PartnerProduct.objects.none()
    
    # Фильтрация по брендам (множественный выбор)
    if brand_slugs:
        brand_names = []
        for brand_slug in brand_slugs:
            try:
                brand = Category.objects.get(slug=brand_slug, category_type='brand')
                brand_names.append(brand.name)
            except Category.DoesNotExist:
                continue
        
        if brand_names:
            query = Q()
            for brand_name in brand_names:
                query |= Q(producer__iexact=brand_name)
            products = products.filter(query)

    # Получаем ОГРАНИЧЕННУЮ структуру категорий
    main_categories = Category.objects.filter(
        parent__isnull=True, 
        category_type='main',
        display=True,
        slug='bytovaya-tekhnika-i-elektronika'  # Только наша категория
    ).order_by('sort_order')

    # Получаем подкатегории и бренды для текущей категории
    subcategories = []
    brands = []

    if current_category and current_category.category_type != 'brand':
        subcategories = current_category.children.filter(
            display=True,
            category_type='sub'
        ).order_by('sort_order')
        
        brand_categories = Category.objects.filter(
            category_type='brand',
            display=True
        )
        
        valid_brands = []
        for brand in brand_categories:
            brand_products_count = products.filter(producer__iexact=brand.name).count()
            if brand_products_count > 0:
                brand.product_count = brand_products_count
                valid_brands.append(brand)
        
        brands = valid_brands

    # Пагинация
    page_size = request.GET.get('page_size', '20')
    try:
        page_size = int(page_size)
    except (ValueError, TypeError):
        page_size = 20

    allowed_page_sizes = [20, 40, 60, 100]
    if page_size not in allowed_page_sizes:
        page_size = 20

    paginator = Paginator(products, page_size)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'catalog/catalog.html', {
        'products': page_obj,
        'page_obj': page_obj,
        'main_categories': main_categories,
        'current_category': current_category,
        'current_brand': current_brand,
        'subcategories': subcategories,
        'brands': brands,
        'search_query': search_query,
        'min_price': min_price,
        'max_price': max_price,
        'selected_brands': brand_slugs,
    })

def product_detail(request, product_key):
    product = get_object_or_404(PartnerProduct, product_key=product_key)
    
    # Получаем все изображения товара
    images = product.uploaded_images.all()

    return render(request, 'catalog/product_detail.html', {
        'product': product,
        'images': images
    })

def add_to_cart(request):
    """Добавление товара в корзину (AJAX)"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_key = data.get('product_key')
            quantity = int(data.get('quantity', 1))
            
            product = get_object_or_404(PartnerProduct, product_key=product_key)
            
            # Получаем или создаем корзину в сессии
            cart = request.session.get('cart', {})
            
            if product_key in cart:
                cart[product_key]['quantity'] += quantity
            else:
                cart[product_key] = {
                    'name': product.name,
                    'price': str(product.price),
                    'quantity': quantity,
                    'image_url': product.main_image.image.url if product.main_image else ''
                }
            
            request.session['cart'] = cart
            request.session.modified = True
            
            # Подсчитываем общее количество товаров в корзине
            total_items = sum(item['quantity'] for item in cart.values())
            
            return JsonResponse({
                'success': True,
                'message': f'Товар "{product.name}" добавлен в корзину',
                'total_items': total_items
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
    total_items = sum(item['quantity'] for item in cart.values())
    return JsonResponse({'total_items': total_items})

def catalog_list(request):
    """Альтернативный вид каталога"""
    # Также ограничиваем товары для этой view
    limited_main_category = Category.objects.filter(
        slug='bytovaya-tekhnika-i-elektronika',
        category_type='main'
    ).first()
    
    if limited_main_category:
        all_limited_categories = get_all_child_categories(limited_main_category)
        all_limited_categories.append(limited_main_category)
        products = PartnerProduct.objects.filter(category__in=all_limited_categories)
    else:
        products = PartnerProduct.objects.none()
    
    # Фильтр по наличию
    availability = request.GET.get('availability')
    if availability == 'in_stock':
        products = products.filter(availability=True)
    elif availability == 'out_of_stock':
        products = products.filter(availability=False)

    # Фильтр по цене
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    # Сортировка
    sort_by = request.GET.get('sort')
    if sort_by == 'name_asc':
        products = products.order_by('name')
    elif sort_by == 'name_desc':
        products = products.order_by('-name')
    elif sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    else:
        products = products.order_by('-id')

    # Пагинация
    paginator = Paginator(products, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'catalog/list.html', {
        'page_obj': page_obj,
        'products': page_obj.object_list,
        'filters': request.GET
    })

def category_detail(request, category_code):
    """Товары в категории"""
    data = get_products_by_category(category_code)
    products = []
    for item in data.get('result', []):
        prod = item['product']
        price = item['price']['order']['value'] if item['price']['order'] else 0
        products.append({
            'product_key': prod['productKey'],
            'name': prod.get('itemNameRus') or prod['itemName'],
            'price': price,
            'available': item['isAvailableForOrder'],
        })
    return render(request, 'catalog/category.html', {
        'products': products,
        'category_code': category_code
    })

def catalog_by_category(request, category_code):
    """Каталог по коду категории"""
    products = PartnerProduct.objects.filter(category_code=category_code)
    return render(request, 'catalog/list.html', {'products': products})

def debug_ocs(request):
    """Отладочная страница для OCS"""
    products_data = get_products_by_category('TV')
    return render(request, 'debug_ocs.html', {'products': products_data.get('result', [])})

@csrf_exempt
def home_fixed(request):
    """Исправленная главная страница"""
    products = Product.objects.all()[:12]
    categories = Category.objects.filter(display=True)
    
    context = {
        'products': products,
        'categories': categories,
        'products_count': products.count(),
    }
    return render(request, 'main/home.html', context)

@csrf_exempt  
def catalog_fixed(request):
    """Исправленная страница каталога"""
    products = Product.objects.all()
    categories = Category.objects.filter(display=True)
    
    context = {
        'products': products,
        'categories': categories,
        'products_count': products.count(),
    }
    return render(request, 'main/home.html', context)

@csrf_exempt
def test_products_fixed(request):
    """Исправленная тестовая страница"""
    products = Product.objects.all()[:10]
    
    context = {
        'products': products,
        'products_count': Product.objects.count(),
    }
    return render(request, 'catalog/test_products.html', context)

def simple_list(request):
    """Простой список товаров"""
    from .models import Product
    products = Product.objects.all()[:20]
    return render(request, 'catalog/simple_list.html', {
        'products': products
    })

@csrf_exempt
def home(request):
    """Главная страница - используем существующую home_fixed"""
    return home_fixed(request)

@csrf_exempt  
def product_list(request):
    """Страница каталога - используем существующую catalog_fixed"""
    return catalog_fixed(request)