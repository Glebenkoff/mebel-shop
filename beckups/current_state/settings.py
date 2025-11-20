import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

SECRET_KEY = 'django-insecure-premium-shop-' + os.urandom(32).hex()[:50]
DEBUG = True  # Убедимся что DEBUG=True
ALLOWED_HOSTS = ['*']  # Для разработки разрешаем все хосты

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    
    # Наши приложения
    'accounts',
    'catalog',
    'cart',
    'main',
    'pages',
    'blog',
    'chat',
    'reviews',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'urls'

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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Настройки аутентификации
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# === EMAIL НАСТРОЙКИ ===

# Для тестирования - письма выводятся в консоль
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Для реальной отправки (раскомментируйте позже):
"""
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yandex.ru'  # Или smtp.gmail.com, smtp.mail.ru
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'ваш-email@yandex.ru'
EMAIL_HOST_PASSWORD = 'ваш-пароль-приложения'
DEFAULT_FROM_EMAIL = 'MebelShop <ваш-email@yandex.ru>'
"""

# Настройки сайта для абсолютных URL
SITE_URL = 'http://127.0.0.1:8000'