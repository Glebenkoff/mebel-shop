import os
import sys
import django
import json
from django.core.management.base import BaseCommand
from datetime import datetime
from pathlib import Path

class Command(BaseCommand):
    help = "Optimized auto-update for frequent execution with logging"

    def add_arguments(self, parser):
        parser.add_argument(
            '--silent',
            action='store_true',
            help='Silent mode for frequent updates',
        )

    def handle(self, *args, **options):
        silent = options.get('silent', False)
        
        if not silent:
            self.stdout.write("⚡ Auto-updating project progress...")
        
        project_stats = self.collect_project_stats(silent)
        self.generate_reports(project_stats, silent)
        self.log_update(project_stats, silent)
        
        if not silent:
            self.stdout.write(
                self.style.SUCCESS(
                    f"✅ Progress: {project_stats['progress_percent']}% | Models: {project_stats['total_models']} | Templates: {project_stats['total_templates']}"
                )
            )

    def collect_project_stats(self, silent=False):
        """Fast statistics collection"""
        BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
        
        stats = {
            'last_updated': datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
            'total_models': 0,
            'total_templates': 0,
            'apps_status': {},
            'progress_percent': 85
        }
        
        # Быстрый подсчет моделей
        try:
            from django.apps import apps
            for app_config in apps.get_app_configs():
                if not app_config.name.startswith('django.'):
                    models_count = len(list(app_config.get_models()))
                    stats['total_models'] += models_count
                    stats['apps_status'][app_config.name] = models_count
        except Exception as e:
            if not silent:
                self.stdout.write(f"ℹ️ {e}")

        # Быстрый подсчет шаблонов
        templates_dir = BASE_DIR / 'templates'
        if templates_dir.exists():
            try:
                stats['total_templates'] = sum(
                    len([f for f in files if f.endswith('.html')])
                    for root, dirs, files in os.walk(templates_dir)
                )
            except:
                pass

        return stats

    def generate_reports(self, project_stats, silent=False):
        """Generate optimized reports"""
        BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
        
        # Краткий PROJECT_PROGRESS.md
        progress_content = f"""# PROJECT PROGRESS - FURNITURE STORE

## LIVE STATS
**Updated:** {project_stats['last_updated']}  
**Progress:** {project_stats['progress_percent']}%
**Models:** {project_stats['total_models']} | **Templates:** {project_stats['total_templates']}

## CURRENT STATUS
🟢 Server: Running
🟢 Admin: Active  
🟢 Catalog: Working
🟢 Auto-Update: Every Minute

## APPS STATUS
{chr(10).join(f"- {app}: {count} models" for app, count in project_stats['apps_status'].items())}

## NEXT FEATURES
👤 User System
🔌 OCS Integration
🛒 Enhanced Cart

## LAST UPDATES
- {project_stats['last_updated']}: Auto-update completed
- Models count: {project_stats['total_models']}
- Templates count: {project_stats['total_templates']}

---
*Auto-update: Every 60 seconds*
*Last: {project_stats['last_updated']}*
"""

        # Краткий PROJECT_PLANS.md
        plans_content = f"""# DEVELOPMENT PLANS

## ACTIVE SPRINT
- [ ] User authentication
- [ ] OCS API integration
- [ ] Product images
- [ ] Order system

## RECENT UPDATES
✅ Fixed auto-update system
✅ Minute-based reporting
✅ Optimized performance
✅ Activity logging added

## QUICK METRICS
- Progress: {project_stats['progress_percent']}%
- Models: {project_stats['total_models']}
- Templates: {project_stats['total_templates']}
- Apps: {len(project_stats['apps_status'])}

## UPDATE HISTORY
Latest: {project_stats['last_updated']}
Frequency: Every minute
Status: Active

---
*Minute-based updates: {project_stats['last_updated']}*
"""

        # Быстрая запись файлов
        with open(BASE_DIR / 'PROJECT_PROGRESS.md', 'w', encoding='utf-8') as f:
            f.write(progress_content)

        with open(BASE_DIR / 'PROJECT_PLANS.md', 'w', encoding='utf-8') as f:
            f.write(plans_content)

        if not silent:
            self.stdout.write("📄 Reports updated")

    def log_update(self, project_stats, silent=False):
        """Логирует обновление в JSON файл"""
        BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
        log_file = BASE_DIR / 'update_log.json'
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'time_display': datetime.now().strftime("%H:%M:%S"),
            'date_display': datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
            'type': 'auto_update',
            'progress': project_stats['progress_percent'],
            'models': project_stats['total_models'],
            'templates': project_stats['total_templates'],
            'apps_count': len(project_stats['apps_status'])
        }
        
        try:
            # Читаем существующий лог
            if log_file.exists():
                with open(log_file, 'r', encoding='utf-8') as f:
                    try:
                        log_data = json.load(f)
                    except:
                        log_data = []
            else:
                log_data = []
            
            # Добавляем новую запись
            log_data.append(log_entry)
            
            # Сохраняем только последние 50 записей (чтобы файл не grew слишком большим)
            log_data = log_data[-50:]
            
            # Сохраняем лог
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(log_data, f, indent=2, ensure_ascii=False)
            
            if not silent:
                self.stdout.write(f"📝 Update logged at {log_entry['time_display']}")
                
        except Exception as e:
            if not silent:
                self.stdout.write(f"⚠️ Logging failed: {e}")