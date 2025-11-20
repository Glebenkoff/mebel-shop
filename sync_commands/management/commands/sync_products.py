from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Синхронизация товаров'

    def handle(self, *args, **options):
        from catalog.models import Category, Product
        
        self.stdout.write('�� СХЯ Т')
        self.stdout.write('=' * 40)
        
        count_before = Product.objects.count()
        self.stdout.write(f'📦 Товаров до синхронизации: {count_before}')
        
        # бедимся что есть категория
        if Category.objects.count() == 0:
            category = Category.objects.create(
                name='ебель для гостиной',
                description='иваны, кресла, журнальные столики'
            )
            self.stdout.write(f'✅ Создана категория: {category.name}')
        
        if count_before == 0:
            category = Category.objects.first()
            product = Product.objects.create(
                name='омфортный диван',
                category=category,
                price=25000.00,
                description='ягкий диван для гостиной',
                stock=5
            )
            self.stdout.write(f'✅ Создан товар: {product.name} - {product.price} руб.')
        
        count_after = Product.objects.count()
        self.stdout.write(f'📦 Товаров после синхронизации: {count_after}')
        self.stdout.write('✅ Синхронизация товаров завершена!')
