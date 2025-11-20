# check_ocs_settings.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.conf import settings

print("=== Проверка настроек OCS ===")
print(f"OCS_API_URL: {settings.OCS_API_URL}")
print(f"OCS_API_KEY: {settings.OCS_API_KEY[:10]}...")  # Покажем только начало ключа
print(f"OCS_API_CONFIG: {settings.OCS_API_CONFIG}")

# Проверим существование товара
from catalog.models import PartnerProduct
try:
    product = PartnerProduct.objects.get(product_key="1000562330")
    print(f"\n=== Информация о товаре ===")
    print(f"ID: {product.id}")
    print(f"Product Key: {product.product_key}")
    print(f"OCS Item ID: {product.ocs_item_id}")
    print(f"Name: {product.name}")
    print(f"Uploaded Images: {product.uploaded_images.count()}")
except PartnerProduct.DoesNotExist:
    print("❌ Товар с product_key='1000562330' не найден!")