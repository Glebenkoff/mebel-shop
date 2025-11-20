from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('search/', views.product_search, name='product_search'),
    path('search/autocomplete/', views.search_autocomplete, name='search_autocomplete'),
    path('<int:id>/', views.product_detail, name='product_detail'),
    # Избранное и сравнение
    path('wishlist/toggle/<int:product_id>/', views.wishlist_toggle, name='wishlist_toggle'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('comparison/toggle/<int:product_id>/', views.comparison_toggle, name='comparison_toggle'),
    path('comparison/', views.comparison_view, name='comparison'),
    path('ajax/wishlist/toggle/<int:product_id>/', views.ajax_wishlist_toggle, name='ajax_wishlist_toggle'),
    path('ajax/comparison/toggle/<int:product_id>/', views.ajax_comparison_toggle, name='ajax_comparison_toggle'),
]
