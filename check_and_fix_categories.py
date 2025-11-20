import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mebel_shop.settings')
django.setup()

from catalog.models import Category

def check_categories():
    """Проверяет текущие категории и их slug'ы"""
    print("=== ПРОВЕРКА КАТЕГОРИЙ ===")
    
    categories = Category.objects.all()
    print(f"Всего категорий: {categories.count()}")
    
    # Проверяем уникальность slug'ов
    slugs = {}
    duplicates = []
    
    for cat in categories:
        if cat.slug in slugs:
            duplicates.append(cat.slug)
        slugs[cat.slug] = slugs.get(cat.slug, 0) + 1
    
    if duplicates:
        print(f"Найдены дублирующиеся slug'ы: {set(duplicates)}")
    else:
        print("Все slug'ы уникальны ✓")
    
    # Выводим структуру
    print("\n=== СТРУКТУРА КАТЕГОРИЙ ===")
    main_cats = Category.objects.filter(parent__isnull=True)
    for main_cat in main_cats:
        print_structure(main_cat)

def print_structure(category, level=0):
    indent = "  " * level
    print(f"{indent}└─ {category.name} (slug: {category.slug})")
    
    for child in category.children.all().order_by('sort_order'):
        print_structure(child, level + 1)

if __name__ == "__main__":
    check_categories()