from .models import Category

def categories(request):
    return {
        'categories': Category.objects.filter(is_active=True)
    }

def search_form(request):
    return {
        'search_query': request.GET.get('q', '')
    }
