from django.core.management.base import BaseCommand
from django.urls import get_resolver
import os

class Command(BaseCommand):
    help = 'Create project structure report'
    
    def handle(self, *args, **options):
        self.stdout.write('=== PROJECT STRUCTURE REPORT ===')
        
        # URLs
        self.stdout.write('\n--- URL PATTERNS ---')
        resolver = get_resolver()
        
        def print_urls(url_patterns, prefix=''):
            for pattern in url_patterns:
                if hasattr(pattern, 'url_patterns'):
                    # This is an include
                    print_urls(pattern.url_patterns, prefix + str(pattern.pattern))
                else:
                    self.stdout.write(f'{prefix + str(pattern.pattern)}')
        
        print_urls(resolver.url_patterns)
        
        # Apps
        self.stdout.write('\n--- INSTALLED APPS ---')
        from django.apps import apps
        for app in apps.get_app_configs():
            self.stdout.write(f'{app.name}')
        
        # Directory structure
        self.stdout.write('\n--- DIRECTORY STRUCTURE ---')
        for root, dirs, files in os.walk('.'):
            level = root.replace('.', '').count(os.sep)
            indent = ' ' * 2 * level
            self.stdout.write(f'{indent}{os.path.basename(root)}/')
            subindent = ' ' * 2 * (level + 1)
            for file in files[:5]:  # Show first 5 files per directory
                if file.endswith(('.py', '.html', '.css', '.js')):
                    self.stdout.write(f'{subindent}{file}')
        
        self.stdout.write(self.style.SUCCESS('Report completed'))
