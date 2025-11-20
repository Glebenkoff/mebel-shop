"""
МИНИМАЛЬНЫЕ НАСТРОЙКИ DJANGO - для диагностики
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).parent

SECRET_KEY = 'minimal-test-key-for-debugging'
DEBUG = True
ALLOWED_HOSTS = ['localhost']

# ТОЛЬКО базовые приложения Django
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'test_db.sqlite3',
    }
}

TIME_ZONE = 'UTC'
USE_TZ = True