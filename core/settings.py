"""
НАСТРОЙКИ DJANGO - ИСПРАВЛЕННАЯ ВЕРСИЯ
Все настройки в ВЕРХНЕМ РЕГИСТРЕ
"""

import os
from pathlib import Path

# Базовая директория проекта
BASE_DIR = Path(__file__).resolve().parent

# Секретный ключ
SECRET_KEY = 'django-insecure-your-secret-key-here'

# Режим отладки
DEBUG = True

# Разрешенные хосты
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Установленные приложения
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Мои приложения
    'accounts',
    'catalog',
    'cart',
    'pages',
    'main',
    'appliances',
    'core',
    'orders',
    'sync_commands',
]

# Промежуточное ПО
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Корневой URLconf
ROOT_URLCONF = 'urls'

# Шаблоны
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# База данных
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Валидация паролей
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Интернационализация
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

# Статические файлы
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Медиа файлы
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Тип поля первичного ключа по умолчанию
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Кастомная модель пользователя
AUTH_USER_MODEL = 'accounts.CustomUser'