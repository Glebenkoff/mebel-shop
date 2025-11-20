from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Синхронизация категорий'

    def handle(self, *args, **options):
        from catalog.models import Category
        
        self.stdout.write('🔄 СХЯ Т')
        self.stdout.write('=' * 40)
        
        count_before = Category.objects.count()
        self.stdout.write(f'📊 атегорий до синхронизации: {count_before}')
        
        if count_before == 0:
            category = Category.objects.create(
                name='ебель для гостиной',
                description='иваны, кресла, журнальные столики'
            )
            self.stdout.write(f'✅ Создана категория: {category.name}')
        
        count_after = Category.objects.count()
        self.stdout.write(f'📊 атегорий после синхронизации: {count_after}')
        self.stdout.write('✅ Синхронизация категорий завершена!')
