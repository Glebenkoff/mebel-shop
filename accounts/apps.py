from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
    
    def ready(self):
        # Отключаем сигнал обновления last_login
        from django.contrib.auth import user_logged_in
        from django.contrib.auth.models import update_last_login
        user_logged_in.disconnect(update_last_login)