# use_db_sessions.py
with open('settings.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Заменяем файловые сессии на базу данных
new_content = content.replace(
    "SESSION_ENGINE = 'django.contrib.sessions.backends.file'",
    "SESSION_ENGINE = 'django.contrib.sessions.backends.db'"
)

with open('settings.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Сессии переключены на базу данных!")