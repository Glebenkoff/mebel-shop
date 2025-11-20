from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

app_name = 'catalog'

urlpatterns = [
    # Главная страница каталога (техника из OCS)
    path('', views.catalog_view, name='product_list'),
    
    # Остальные маршруты каталога
    path('catalog/', csrf_exempt(views.catalog_fixed), name='catalog'),
    path('test-fixed/', views.test_products_fixed, name='test_fixed'),
    path('simple/', views.catalog_list, name='simple_list'),
    path('catalog-view/', views.catalog_view, name='catalog_view'),
    path('product/<str:product_key>/', views.product_detail, name='product_detail'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('get-cart-count/', views.get_cart_count, name='get_cart_count'),
    path('category/<str:category_code>/', views.category_detail, name='category_detail'),
    path('catalog-by-category/<str:category_code>/', views.catalog_by_category, name='catalog_by_category'),
    path('debug-ocs/', views.debug_ocs, name='debug_ocs'),
]
