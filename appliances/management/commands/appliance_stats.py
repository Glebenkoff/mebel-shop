from django.core.management.base import BaseCommand
from appliances.models import ApplianceCategory, ApplianceProduct

class Command(BaseCommand):
    help = 'Show appliances statistics'
    
    def handle(self, *args, **options):
        self.stdout.write('=== APPLIANCES STATISTICS ===')
        
        # Statistics
        categories_count = ApplianceCategory.objects.count()
        products_count = ApplianceProduct.objects.count()
        products_with_price = ApplianceProduct.objects.filter(price__isnull=False).count()
        
        self.stdout.write('Categories: ' + str(categories_count))
        self.stdout.write('Products: ' + str(products_count))
        self.stdout.write('Products with price: ' + str(products_with_price))
        
        # Show top categories
        self.stdout.write('\n--- Top Categories ---')
        categories = ApplianceCategory.objects.all()[:10]
        for category in categories:
            product_count = ApplianceProduct.objects.filter(category=category).count()
            self.stdout.write(category.code + ': ' + category.name + ' (' + str(product_count) + ' products)')
        
        # Show sample products
        self.stdout.write('\n--- Sample Products ---')
        products = ApplianceProduct.objects.all()[:5]
        for product in products:
            self.stdout.write('Name: ' + product.name)
            self.stdout.write('  Category: ' + product.category.name)
            self.stdout.write('  Producer: ' + (product.producer or 'N/A'))
            self.stdout.write('  Price: ' + (str(product.price) if product.price else 'No price'))
            self.stdout.write('  Stock: ' + str(product.stock))
            self.stdout.write('')
        
        self.stdout.write(self.style.SUCCESS('Statistics check completed'))
