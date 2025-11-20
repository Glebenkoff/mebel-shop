import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from cart.models import Cart
from django.contrib.auth import get_user_model

User = get_user_model()

# Находим пользователей с несколькими корзинами
users_with_multiple_carts = User.objects.annotate(
    cart_count=models.Count('cart')
).filter(cart_count__gt=1)

print(f"Найдено пользователей с несколькими корзинами: {users_with_multiple_carts.count()}")

for user in users_with_multiple_carts:
    carts = Cart.objects.filter(user=user)
    print(f"Пользователь {user.username}: {carts.count()} корзин")
    
    # Оставляем только первую корзину, остальные удаляем
    if carts.count() > 1:
        keep_cart = carts.first()
        delete_carts = carts.exclude(id=keep_cart.id)
        delete_count = delete_carts.count()
        delete_carts.delete()
        print(f"  Удалено {delete_count} дубликатов, оставлена корзина ID: {keep_cart.id}")

print("Дубликаты корзин очищены!")