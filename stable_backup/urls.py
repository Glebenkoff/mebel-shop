from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.shortcuts import render
from catalog.models import Category, Product
from blog.models import Article

def home(request):
    categories = Category.objects.all()[:6]
    products = Product.objects.filter(available=True)[:6]
    latest_articles = Article.objects.filter(status='published')[:3]
    
    return render(request, 'main/home.html', {
        'categories': categories,
        'products': products,
        'latest_articles': latest_articles
    })

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('catalog/', include('catalog.urls')),
    path('cart/', include('cart.urls')),
    path('pages/', include('pages.urls')),
    path('reviews/', include('reviews.urls')),
    path('blog/', include('blog.urls')),
]