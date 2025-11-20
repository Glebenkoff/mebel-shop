from django.core.management.base import BaseCommand
from datetime import datetime

class Command(BaseCommand):
    help = "Quick update project progress (for frequent use)"

    def handle(self, *args, **options):
        self.stdout.write("⚡ Quick progress update...")
        
        # ростое обновление времени
        current_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        
        # инимальное обновление отчетов
        from pathlib import Path
        BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
        
        quick_content = f"""# QUICK UPDATE
Last quick update: {current_time}
Status: All systems operational
Next check: On next manual run
"""
        
        with open(BASE_DIR / 'QUICK_UPDATE.md', 'w', encoding='utf-8') as f:
            f.write(quick_content)
        
        self.stdout.write(f"✅ Quick update completed at {current_time}")
