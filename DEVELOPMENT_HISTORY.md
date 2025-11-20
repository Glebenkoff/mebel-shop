ИСТОРИЯ РАЗРАБОТКИ:

1. Создана структура management commands в catalog/management/commands/
2. Решена проблема с нулевыми байтами в файлах
3. Созданы команды для работы с данными:
   - check_catalog, catalog_stats, show_products
   - create_test_categories, create_simple_products
   - export_csv, fix_empty_categories
4. База содержит тестовые данные: 10 категорий, 20 товаров
5. Все команды проверены и работают
