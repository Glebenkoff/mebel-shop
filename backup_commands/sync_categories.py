from django.core.management.base import BaseCommand
from catalog.api import get_categories
from catalog.models import Category
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Синхронизация категорий из OCS API'
    
    def handle(self, *args, **options):
        self.stdout.write('🔄 Получение категорий из API OCS...')
        
        try:
            categories_data = get_categories()
            synced_count = self.sync_categories(categories_data)
            
            self.stdout.write(
                self.style.SUCCESS(f'✅ Успешно синхронизировано {synced_count} категорий!')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Ошибка при загрузке категорий: {e}')
            )
    
    def sync_categories(self, categories_data, parent=None):
        """Рекурсивная синхронизация категорий"""
        count = 0
        
        for cat_data in categories_data:
            # Определяем тип категории
            if parent is None:
                category_type = 'main'
            elif cat_data.get('children'):
                category_type = 'sub' 
            else:
                category_type = 'sub'  # Или 'product' если это конечная товарная категория
            
            # Создаем или обновляем категорию
            category, created = Category.objects.update_or_create(
                ocs_category_code=cat_data['category'],
                defaults={
                    'name': cat_data['name'],
                    'slug': cat_data['category'].lower(),
                    'parent': parent,
                    'category_type': category_type,
                    'display': True,
                    'sort_order': 0,
                }
            )
            
            if created:
                self.stdout.write(f'✅ Добавлена: {category.name} ({category.ocs_category_code})')
            else:
                self.stdout.write(f'📝 Обновлена: {category.name}')
            
            count += 1
            
            # Рекурсивно обрабатываем дочерние категории
            if cat_data.get('children'):
                count += self.sync_categories(cat_data['children'], category)
        
        return count