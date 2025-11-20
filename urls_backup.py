from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

app_name = 'catalog'

urlpatterns = [
    # Главная страница каталога
    path('', views.catalog_view, name='product_list'),
    
    # Детальная страница товара
    path('product/<str:product_key>/', views.product_detail, name='product_detail'),
    
    # Страница категории
    path('category/<str:category_code>/', views.category_detail, name='category_detail'),
    
    # API для корзины
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('get-cart-count/', views.get_cart_count, name='get_cart_count'),
    
    # Отладка
    path('debug-ocs/', views.debug_ocs, name='debug_ocs'),
    
    # Альтернативные маршруты для совместимости
    path('catalog/', views.catalog_view, name='catalog'),
    path('simple/', views.catalog_list, name='simple_list'),
    path('catalog-by-category/<str:category_code>/', views.catalog_by_category, name='catalog_by_category'),
]