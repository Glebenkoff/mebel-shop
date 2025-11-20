# clean_session_settings.py
with open('settings.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Удаляем все старые настройки сессий и добавляем чистые
new_lines = []
skip_next = False

for line in lines:
    if 'SESSION_' in line:
        skip_next = True
        continue
    elif skip_next and line.strip() == '':
        skip_next = False
        continue
    elif not skip_next:
        new_lines.append(line)

# Добавляем чистые настройки в конец
new_lines.append('\n# Настройки сессий\n')
new_lines.append('SESSION_ENGINE = \'django.contrib.sessions.backends.db\'\n')
new_lines.append('SESSION_COOKIE_AGE = 1209600  # 2 недели\n')
new_lines.append('SESSION_SAVE_EVERY_REQUEST = True\n')
new_lines.append('SESSION_EXPIRE_AT_BROWSER_CLOSE = False\n')

with open('settings.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Настройки сессий очищены и перезаписаны!")