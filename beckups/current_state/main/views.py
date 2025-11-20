from django.shortcuts import render
from blog.models import Article

def home(request):
    latest_articles = Article.objects.filter(is_published=True)[:3]
    return render(request, 'main/home.html', {
        'latest_articles': latest_articles
    })