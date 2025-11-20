from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Review
from .forms import ReviewForm

@login_required
@csrf_exempt
def add_review(request, product_id):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product_id = product_id
            review.user = request.user
            review.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Отзыв успешно добавлен!',
                'review': {
                    'user': request.user.username,
                    'rating': review.rating,
                    'text': review.text,
                    'created_at': review.created_at.strftime('%d.%m.%Y'),
                    'is_approved': review.is_approved
                }
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
    
    return JsonResponse({'success': False, 'error': 'Неверный метод запроса'})