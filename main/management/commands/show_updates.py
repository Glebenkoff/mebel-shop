from django.core.management.base import BaseCommand
import json
from pathlib import Path
from datetime import datetime

class Command(BaseCommand):
    help = "Show update logs and statistics"

    def add_arguments(self, parser):
        parser.add_argument(
            '--tail',
            type=int,
            default=10,
            help='Show last N entries (default: 10)',
        )
        parser.add_argument(
            '--watch',
            action='store_true',
            help='Watch mode - continuously show new entries',
        )

    def handle(self, *args, **options):
        tail_count = options['tail']
        watch_mode = options['watch']
        
        log_file = Path(__file__).resolve().parent.parent.parent.parent / 'update_log.json'
        
        if not log_file.exists():
            self.stdout.write("ℹ️ No update logs found yet. Wait for first auto-update.")
            return
        
        def show_logs():
            with open(log_file, 'r', encoding='utf-8') as f:
                log_data = json.load(f)
            
            # оказываем последние записи
            recent_logs = log_data[-tail_count:]
            
            self.stdout.write(f"📊 Last {len(recent_logs)} updates:")
            self.stdout.write("-" * 50)
            
            for log in recent_logs:
                self.stdout.write(
                    f"🕐 {log['time_display']} | "
                    f"Progress: {log['progress']}% | "
                    f"Models: {log['models']} | "
                    f"Templates: {log['templates']}"
                )
            
            # Статистика
            if len(log_data) > 1:
                first = datetime.fromisoformat(log_data[0]['timestamp'])
                last = datetime.fromisoformat(log_data[-1]['timestamp'])
                total_time = (last - first).total_seconds() / 60  # в минутах
                updates_per_minute = len(log_data) / total_time if total_time > 0 else 0
                
                self.stdout.write("-" * 50)
                self.stdout.write(f"📈 Statistics:")
                self.stdout.write(f"   Total updates: {len(log_data)}")
                self.stdout.write(f"   Time span: {total_time:.1f} minutes")
                self.stdout.write(f"   Updates/minute: {updates_per_minute:.2f}")
        
        if watch_mode:
            self.stdout.write("👀 Watching update logs... (Ctrl+C to stop)")
            import time
            try:
                while True:
                    show_logs()
                    self.stdout.write("\n" + "="*50 + "\n")
                    time.sleep(30)  # бновляем каждые 30 секунд
            except KeyboardInterrupt:
                self.stdout.write("\n🛑 Stopped watching")
        else:
            show_logs()
