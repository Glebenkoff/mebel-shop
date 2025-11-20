from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Простая команда синхронизации'

    def handle(self, *args, **options):
        self.stdout.write('✅ Новая команда синхронизации работает!')
        
        # Проверяем доступ к моделям
        try:
            from catalog.models import Category, Product
            categories = Category.objects.count()
            products = Product.objects.count()
            self.stdout.write(f'📊 Категории: {categories}, Товары: {products}')
        except Exception as e:
            self.stdout.write(f'⚠️  Ошибка доступа к моделям: {e}')