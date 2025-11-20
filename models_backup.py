from django.db import models
from django.utils.text import slugify
from django.utils import timezone
import os

def product_image_path(instance, filename):
    """Путь для сохранения изображений товаров"""
    return f'products/{instance.product.product_key}/{filename}'

class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название категории")
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    display = models.BooleanField(default=True, verbose_name="Отображать в каталоге")
    image = models.ImageField(upload_to='categories/', null=True, blank=True)
    sort_order = models.PositiveIntegerField(default=0, verbose_name="Порядок сортировки")
    
    # Новые поля для интеграции с OCS
    ocs_category_code = models.CharField("Код в OCS", max_length=20, blank=True, null=True, unique=True)
    last_sync_date = models.DateTimeField(null=True, blank=True)
    
    # Поле для определения типа категории
    CATEGORY_TYPE_CHOICES = [
        ('main', 'Основная категория'),
        ('sub', 'Подкатегория'),
        ('brand', 'Производитель'),
    ]
    category_type = models.CharField(
        "Тип категории", 
        max_length=10, 
        choices=CATEGORY_TYPE_CHOICES, 
        default='main'
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['sort_order']

    def __str__(self):
        return self.name
    
    def is_main_category(self):
        return self.category_type == 'main' and self.parent is None
    
    def is_subcategory(self):
        return self.category_type == 'sub' and self.parent is not None
    
    def is_brand(self):
        return self.category_type == 'brand'
    
    def get_limited_main_categories(self):
        """Получает только ограниченный набор основных категорий"""
        return Category.objects.filter(
            parent__isnull=True, 
            category_type='main',
            display=True,
            slug='bytovaya-tekhnika-i-elektronika'
        ).order_by('sort_order')
    
    def get_brands(self):
        """Получить производителей для этой категории/подкатегории"""
        from .models import PartnerProduct
        
        if self.category_type == 'main':
            # Для основной категории - бренды всех подкатегорий
            subcategories = self.children.filter(category_type='sub')
            brand_ids = PartnerProduct.objects.filter(
                category__in=subcategories
            ).values_list('producer', flat=True).distinct()
        elif self.category_type == 'sub':
            # Для подкатегории - бренды этой подкатегории
            brand_ids = PartnerProduct.objects.filter(
                category=self
            ).values_list('producer', flat=True).distinct()
        else:
            return []
        
        # Создаем объекты Category для брендов
        brands = []
        for brand_name in brand_ids:
            if brand_name:
                slug = f"brand-{slugify(brand_name)}"
                brand, created = Category.objects.get_or_create(
                    slug=slug,
                    defaults={
                        'name': brand_name,
                        'category_type': 'brand',
                        'parent': self,
                        'sort_order': 0
                    }
                )
                brands.append(brand)
        
        return brands

    def update_sync_date(self):
        """Обновляет дату синхронизации"""
        self.last_sync_date = timezone.now()
        self.save()

class PartnerProduct(models.Model):
    # Основные поля
    name = models.CharField(max_length=500, verbose_name="Название товара")
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена", default=0)
    
    # Поля для связи с OCS
    ocs_item_id = models.CharField("ID в OCS", max_length=50, unique=True, blank=True, null=True)  # ИСПРАВЛЕНО
    product_key = models.CharField("Ключ товара", max_length=100, blank=True, default="")
    external_id = models.CharField("Внешний ID", max_length=100, blank=True, null=True)
    
    # Информация о товаре
    part_number = models.CharField("Каталожный номер", max_length=100, blank=True)
    producer = models.CharField("Производитель", max_length=200, blank=True)
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        verbose_name="Категория", 
        related_name='partner_products', 
        null=True, 
        blank=True
    )
    
    # Цены и валюта
    original_price = models.DecimalField("Цена OCS", max_digits=10, decimal_places=2, default=0)
    currency = models.CharField("Валюта", max_length=3, default='RUR')
    
    # Изображения
    image_url = models.URLField("Ссылка на изображение", blank=True, null=True)
    content_images = models.JSONField("Изображения из API", default=list, blank=True)
    
    # Характеристики
    properties = models.JSONField("Характеристики", default=dict, blank=True)
    
    # Физические характеристики
    weight = models.DecimalField("Вес", max_digits=8, decimal_places=3, null=True, blank=True)
    volume = models.DecimalField("Объем", max_digits=8, decimal_places=6, null=True, blank=True)
    width = models.DecimalField("Ширина", max_digits=8, decimal_places=3, null=True, blank=True)
    height = models.DecimalField("Высота", max_digits=8, decimal_places=3, null=True, blank=True)
    depth = models.DecimalField("Глубина", max_digits=8, decimal_places=3, null=True, blank=True)
    
    # Технические поля
    warranty = models.CharField("Гарантия", max_length=100, blank=True)
    min_order_quantity = models.IntegerField("Мин. кол-во заказа", default=1)
    availability = models.BooleanField("В наличии", default=True)
    is_active = models.BooleanField("Активный", default=True)
    
    # Данные синхронизации
    ocs_data = models.JSONField("Данные OCS", default=dict, blank=True)
    last_sync_date = models.DateTimeField(null=True, blank=True)
    sync_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Ожидает'),
            ('synced', 'Синхронизирован'), 
            ('error', 'Ошибка'),
            ('out_of_stock', 'Нет в наличии')
        ],
        default='pending',
        verbose_name="Статус синхронизации"
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.part_number})" if self.part_number else self.name
    
    def save(self, *args, **kwargs):
        # Автоматически устанавливаем product_key если не задан
        if not self.product_key and self.ocs_item_id:
            self.product_key = self.ocs_item_id
        
        # Автоматически устанавливаем external_id если не задан
        if not self.external_id and self.ocs_item_id:
            self.external_id = self.ocs_item_id
            
        # Обновляем дату синхронизации при сохранении
        if self.sync_status == 'synced' and not self.last_sync_date:
            self.last_sync_date = timezone.now()
            
        super().save(*args, **kwargs)
    
    @property
    def main_image(self):
        """Основное изображение товара"""
        if self.uploaded_images.exists():
            return self.uploaded_images.first()
        return None
    
    def get_price_display(self):
        """Отформатированная цена"""
        return f"{self.price} {self.currency}"
    
    def update_from_ocs_data(self, product_data: dict, content_data: dict = None):
        """Обновление товара из данных OCS"""
        try:
            product_info = product_data.get('product', {})
            
            # Основная информация
            self.name = product_info.get('itemName', '')[:500]
            self.product_key = product_info.get('productKey', self.ocs_item_id)
            self.part_number = product_info.get('partNumber', '')
            self.producer = product_info.get('producer', '')
            self.description = product_info.get('productDescription', '')[:1000]
            
            # Цены
            price_info = product_info.get('price', {})
            order_price = price_info.get('order', {})
            if order_price and order_price.get('value'):
                self.price = order_price.get('value')
                self.original_price = order_price.get('value')
                self.currency = order_price.get('currency', 'RUR')
            
            # Физические характеристики
            packaging_info = product_info.get('packageInformation', {})
            if packaging_info:
                self.weight = packaging_info.get('weight')
                self.volume = packaging_info.get('volume')
                self.width = packaging_info.get('width')
                self.height = packaging_info.get('height')
                self.depth = packaging_info.get('depth')
                self.min_order_quantity = packaging_info.get('minOrderQuantity', 1)
            
            # Гарантия и статус
            self.warranty = product_info.get('warranty', '')
            
            # Определяем доступность
            locations = product_info.get('locations', [])
            self.availability = any(
                loc.get('quantity', {}).get('value', 0) > 0 
                for loc in locations
            )
            
            # Обработка контента (характеристики и изображения)
            if content_data:
                self.properties = content_data.get('properties', [])
                
                # Сохраняем ссылки на изображения
                images = content_data.get('images', [])
                medium_images = content_data.get('mediumImages', [])
                all_images = images + medium_images
                
                self.content_images = [
                    {
                        'url': img.get('url'),
                        'width': img.get('width'),
                        'height': img.get('height'),
                        'order': img.get('order', 0)
                    }
                    for img in all_images[:10]
                ]
            
            # Сохраняем полные данные OCS
            self.ocs_data = product_data
            
            # Обновляем статус
            self.sync_status = 'synced'
            self.last_sync_date = timezone.now()
            self.save()
            
            return True
            
        except Exception as e:
            self.sync_status = 'error'
            self.save()
            print(f"Ошибка обновления товара {self.ocs_item_id}: {e}")
            return False

class ProductImage(models.Model):
    product = models.ForeignKey(PartnerProduct, on_delete=models.CASCADE, related_name='uploaded_images')
    image = models.ImageField(upload_to=product_image_path, blank=True, null=True)
    order = models.IntegerField("Порядок", default=0)
    is_main = models.BooleanField("Основное изображение", default=False)
    image_url = models.URLField("URL изображения", blank=True, null=True)
    
    class Meta:
        verbose_name = "Изображение товара"
        verbose_name_plural = "Изображения товаров"
        ordering = ['-is_main', 'order']
    
    def __str__(self):
        return f"Изображение для {self.product.name}"
    
    def save(self, *args, **kwargs):
        if self.is_main:
            ProductImage.objects.filter(product=self.product, is_main=True).update(is_main=False)
        super().save(*args, **kwargs)

class ContactMessage(models.Model):
    name = models.CharField("Имя", max_length=100)
    email = models.EmailField("Email")
    subject = models.CharField("Тема", max_length=200)
    message = models.TextField("Сообщение")
    created_at = models.DateTimeField("Получено", auto_now_add=True)

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    def __str__(self):
        return f"{self.name} — {self.subject}"

class CategoryMapping(models.Model):
    """Связь между OCS категориями и нашими внутренними категориями"""
    ocs_category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='ocs_mappings',
        verbose_name="Категория OCS"
    )
    our_category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='our_mappings',
        verbose_name="Наша категория"
    )
    is_primary = models.BooleanField(
        "Основное сопоставление", 
        default=True,
        help_text="Если товар может быть в нескольких категориях, это основное отображение"
    )
    
    class Meta:
        verbose_name = "Сопоставление категорий"
        verbose_name_plural = "Сопоставления категорий"
        unique_together = ['ocs_category', 'our_category']
    
    def __str__(self):
        return f"{self.ocs_category.name} → {self.our_category.name}"