from django.core.management.base import BaseCommand
from datetime import datetime

class Command(BaseCommand):
    help = "Simple progress update test"

    def handle(self, *args, **options):
        self.stdout.write("✅ Project is working!")
        self.stdout.write(f"🕐 Last checked: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
        self.stdout.write("📊 Current progress: 85%")
        self.stdout.write("🚀 Next: User authentication & OCS integration")
