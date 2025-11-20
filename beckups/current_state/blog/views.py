from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Article, Category, Comment
from .forms import CommentForm

def article_list(request, category_slug=None):
    categories = Category.objects.all()
    articles = Article.objects.filter(status='published')
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        articles = articles.filter(category=category)
    else:
        category = None
    
    context = {
        'articles': articles,
        'categories': categories,
        'current_category': category,
    }
    return render(request, 'blog/article_list.html', context)

def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug, status='published')
    article.increase_views()
    
    # Комментарии к статье
    comments = article.comments.filter(is_approved=True, parent__isnull=True)
    comment_form = CommentForm()
    
    context = {
        'article': article,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'blog/article_detail.html', context)

@login_required
@csrf_exempt
def add_comment(request, article_id):
    if request.method == 'POST':
        article = get_object_or_404(Article, id=article_id)
        form = CommentForm(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.author = request.user
            comment.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Комментарий успешно добавлен!',
                'comment': {
                    'author': request.user.username,
                    'text': comment.text,
                    'created_at': comment.created_at.strftime('%d.%m.%Y %H:%M'),
                }
            })
        
        return JsonResponse({
            'success': False,
            'errors': form.errors
        })
    
    return JsonResponse({'success': False, 'error': 'Неверный метод'})