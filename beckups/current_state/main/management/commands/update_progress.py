from django.core.management.base import BaseCommand
from datetime import datetime

class Command(BaseCommand):
    help = "Update project progress reports manually"

    def handle(self, *args, **options):
        self.stdout.write("🚀 Manual progress update started...")
        self.stdout.write(f"📅 Last update: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
        self.stdout.write("✅ Use this command instead of auto-update to avoid loops")
        self.stdout.write("💡 Run: python manage.py update_progress")
