from django.db import models

class ApplianceCategory(models.Model):
    # атегории техники
    code = models.CharField(max_length=20, unique=True, verbose_name='од категории')
    name = models.CharField(max_length=255, verbose_name='азвание')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name='одительская категория')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'атегория техники'
        verbose_name_plural = 'атегории техники'

    def __str__(self):
        return f'{self.name} ({self.code})'

class ApplianceProduct(models.Model):
    # Товары техники
    item_id = models.CharField(max_length=50, unique=True, verbose_name='ID товара')
    product_key = models.CharField(max_length=50, verbose_name='люч товара')
    part_number = models.CharField(max_length=100, verbose_name='ртикул')
    name = models.CharField(max_length=500, verbose_name='азвание')
    russian_name = models.CharField(max_length=500, verbose_name='усское название', blank=True)
    
    category = models.ForeignKey(ApplianceCategory, on_delete=models.CASCADE, verbose_name='атегория')
    producer = models.CharField(max_length=255, verbose_name='роизводитель', blank=True)
    brand = models.CharField(max_length=255, verbose_name='ренд', blank=True)
    
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='ена')
    stock = models.IntegerField(default=0, verbose_name='аличие')
    
    description = models.TextField(verbose_name='писание', blank=True)
    warranty = models.TextField(verbose_name='арантия', blank=True)
    
    # ополнительные поля
    line_code = models.CharField(max_length=50, blank=True, verbose_name='од линейки')
    ean128 = models.CharField(max_length=50, blank=True, verbose_name='Штрих-код')
    vat_percent = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='С %')
    
    is_active = models.BooleanField(default=True, verbose_name='ктивный')
    sync_date = models.DateTimeField(auto_now=True, verbose_name='ата синхронизации')
    
    class Meta:
        verbose_name = 'Товар техники'
        verbose_name_plural = 'Товары техники'

    def __str__(self):
        return self.name
