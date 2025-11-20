from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.article_list, name='article_list'),
    path('category/<slug:category_slug>/', views.article_list, name='article_list_by_category'),
    path('article/<slug:slug>/', views.article_detail, name='article_detail'),
    path('comment/add/<int:article_id>/', views.add_comment, name='add_comment'),
]