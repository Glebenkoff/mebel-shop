import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

import django
django.setup()

from cart.models import Cart

# Создаем корзину если ее нет
cart, created = Cart.objects.get_or_create(id=1)
if created:
    print("✅ Корзина создана")
else:
    print("✅ Корзина уже существует")
