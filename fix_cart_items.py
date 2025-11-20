# fix_cart_items.py
import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from cart.models import Cart, CartItem
from django.contrib.auth.models import User

print("=== АНАЛИЗ CART ITEMS ===")

# Проверяем все корзины
carts = Cart.objects.all()
print(f"Всего корзин: {carts.count()}")

for cart in carts:
    # Группируем товары по product_id и считаем дубликаты
    from django.db.models import Count
    duplicate_items = CartItem.objects.filter(cart=cart).values('product').annotate(
        count=Count('id')
    ).filter(count__gt=1)
    
    if duplicate_items.exists():
        print(f"Корзина {cart.id} (пользователь: {cart.user.username}):")
        
        for item in duplicate_items:
            product_id = item['product']
            count = item['count']
            print(f"  Товар {product_id}: {count} дубликатов")
            
            # Получаем все дубликаты этого товара
            duplicates = CartItem.objects.filter(cart=cart, product_id=product_id)
            
            # Оставляем первый, удаляем остальные
            keep_item = duplicates.first()
            delete_items = duplicates.exclude(id=keep_item.id)
            delete_count = delete_items.count()
            
            # Суммируем quantity в оставляемом item
            total_quantity = sum(item.quantity for item in duplicates)
            keep_item.quantity = total_quantity
            keep_item.save()
            
            delete_items.delete()
            print(f"    ✅ Объединено в один item с quantity={total_quantity}, удалено {delete_count} дубликатов")

print("\n=== ПРОВЕРКА РЕЗУЛЬТАТА ===")
for cart in carts:
    duplicate_items = CartItem.objects.filter(cart=cart).values('product').annotate(
        count=Count('id')
    ).filter(count__gt=1)
    
    if duplicate_items.exists():
        print(f"⚠️  Корзина {cart.id} все еще имеет дубликаты: {list(duplicate_items)}")
    else:
        print(f"✅ Корзина {cart.id}: нет дубликатов")

print("\n✅ Все дубликаты CartItem очищены!")