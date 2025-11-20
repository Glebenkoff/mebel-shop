from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'ростая синхронизация и статистика'

    def handle(self, *args, **options):
        from catalog.models import Category, Product
        from cart.models import Cart, CartItem
        from accounts.models import CustomUser
        
        self.stdout.write('🔄 СТЯ СХЯ')
        self.stdout.write('=' * 40)
        
        self.stdout.write(f'📊 атегории: {Category.objects.count()}')
        self.stdout.write(f'📦 Товары: {Product.objects.count()}')
        self.stdout.write(f'🛒 орзины: {Cart.objects.count()}')
        self.stdout.write(f'👤 ользователи: {CustomUser.objects.count()}')
        
        self.stdout.write('✅ Статистика получена успешно!')
