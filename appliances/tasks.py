# appliances/tasks.py
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.management import call_command
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

@shared_task
def sync_appliances_full():
    """Полная синхронизация каталога техники"""
    try:
        logger.info("Starting full appliances sync")
        call_command('sync_appliances_full', '--products-limit', 200)
        logger.info("Full appliances sync completed successfully")
        return "SUCCESS"
    except Exception as e:
        logger.error(f"Full appliances sync failed: {e}")
        return f"ERROR: {e}"

@shared_task
def sync_stock_prices():
    """Синхронизация наличия и цен"""
    try:
        logger.info("Starting stock and prices sync")
        call_command('sync_appliances_stock_prices')
        logger.info("Stock and prices sync completed")
        return "SUCCESS"
    except Exception as e:
        logger.error(f"Stock sync failed: {e}")
        return f"ERROR: {e}"

@shared_task  
def sync_popular_categories():
    """Синхронизация популярных категорий"""
    popular_categories = ['V070000', 'V070101', 'V070102', 'V070100']  # Телевизоры, холодильники, стиральные машины, плиты
    try:
        logger.info("Starting popular categories sync")
        call_command('sync_appliances_full', '--categories', ','.join(popular_categories), '--products-limit', 50)
        logger.info("Popular categories sync completed")
        return "SUCCESS"
    except Exception as e:
        logger.error(f"Popular categories sync failed: {e}")
        return f"ERROR: {e}"