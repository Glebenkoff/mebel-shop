# mebel_shop/celery.py (создаем если нет)
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mebel_shop.settings')

app = Celery('mebel_shop')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Периодические задачи
app.conf.beat_schedule = {
    # Ежедневная полная синхронизация в 3:00 ночи
    'sync-appliances-daily': {
        'task': 'appliances.tasks.sync_appliances_full',
        'schedule': crontab(hour=3, minute=0),
    },
    # Синхронизация наличия каждые 2 часа
    'sync-appliances-stock': {
        'task': 'appliances.tasks.sync_stock_prices',
        'schedule': crontab(hour='*/2'),
    },
    # Синхронизация популярных категорий каждые 6 часов
    'sync-popular-categories': {
        'task': 'appliances.tasks.sync_popular_categories',
        'schedule': crontab(hour='*/6'),
    },
}