# КОНТЕКСТ ПРОЕКТА: МЕБЕЛЬНЫЙ МАГАЗИН

## О ПРОЕКТЕ:
- Django проект мебельного магазина
- Приложение: catalog
- База данных: SQLite с тестовыми данными
- Созданы management commands для администрирования

## КЛЮЧЕВЫЕ КОМАНДЫ:
python manage.py check_catalog - проверка данных
python manage.py catalog_stats - статистика
python manage.py show_products - список товаров
python manage.py fill_test_data - наполнение тестовыми данными

## СТРУКТУРА МОДЕЛЕЙ:
- Category - категории товаров
- PartnerProduct - товары (вместо Product)
- ProductImage - изображения товаров

## ТЕКУЩЕЕ СОСТОЯНИЕ:
- 10 тестовых категорий мебели
- 20 тестовых товаров
- Все management commands работают
