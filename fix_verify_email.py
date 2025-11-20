with open('accounts/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Заменяем проблемную функцию
new_content = content.replace(
'''def verify_email(request, token):
    try:
        user = UserProfile.objects.get(verification_token=token)
        user.email_verified = True
        user.is_active = True
        user.verification_token = ''
        user.save()

        from django.contrib.auth import login
        user.backend = 'django.contrib.auth.backends.ModelBackend'
''',
'''def verify_email(request, token):
    try:
        # Получаем профиль пользователя по токену
        profile = UserProfile.objects.get(verification_token=token)
        user = profile.user  # Получаем самого пользователя
        
        # Активируем пользователя
        user.is_active = True
        user.save()
        
        # Активируем профиль
        profile.email_verified = True
        profile.verification_token = ''
        profile.save()
        
        # ЗАКОММЕНТИРОВАНО для исправления ошибки last_login
        # from django.contrib.auth import login
        # user.backend = 'django.contrib.auth.backends.ModelBackend'
'''
)

with open('accounts/views.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Функция verify_email исправлена!")