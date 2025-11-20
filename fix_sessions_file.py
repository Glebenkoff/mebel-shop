# fix_sessions_file.py
session_settings = '''
# Настройки сессий для "Запомнить меня"
SESSION_ENGINE = 'django.contrib.sessions.backends.file'
SESSION_FILE_PATH = 'C:/tmp/django_sessions'
SESSION_COOKIE_AGE = 1209600  # 2 недели
SESSION_SAVE_EVERY_REQUEST = True
'''

with open('settings.py', 'a', encoding='utf-8') as f:
    f.write(session_settings)

print("Настройки файловых сессий добавлены в settings.py!")