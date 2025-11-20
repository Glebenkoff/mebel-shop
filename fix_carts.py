# fix_carts.py
import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from cart.models import Cart
from django.contrib.auth.models import User

print("=== АНАЛИЗ КОРЗИН ===")

# Проверяем всех пользователей
users = User.objects.all()
print(f"Всего пользователей: {users.count()}")

for user in users:
    carts = Cart.objects.filter(user=user)
    cart_count = carts.count()
    print(f"Пользователь '{user.username}': {cart_count} корзин")
    
    # Если у пользователя больше одной корзины - чиним
    if cart_count > 1:
        print(f"  ⚠️  Найдено {cart_count} корзин! Удаляем дубликаты...")
        
        # Оставляем первую корзину (самую старую), удаляем остальные
        keep_cart = carts.first()
        delete_carts = carts.exclude(id=keep_cart.id)
        delete_count = delete_carts.count()
        
        delete_carts.delete()
        print(f"  ✅ Удалено {delete_count} дубликатов, оставлена корзина ID: {keep_cart.id}")

print("\n=== ПРОВЕРКА РЕЗУЛЬТАТА ===")
for user in users:
    carts = Cart.objects.filter(user=user)
    print(f"Пользователь '{user.username}': {carts.count()} корзин")

print("\n✅ Все дубликаты корзин очищены!")