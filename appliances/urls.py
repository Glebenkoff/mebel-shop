from django.urls import path
from . import views

app_name = 'appliances'

urlpatterns = [
    path('', views.appliance_list, name='appliance_list'),
    path('categories/', views.category_list, name='category_list'),
    path('product/<str:item_id>/', views.appliance_detail, name='appliance_detail'),
    path('api/stats/', views.api_stats, name='api_stats'),
]
