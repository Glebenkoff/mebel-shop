# update_login_view.py
with open('accounts/urls.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Заменяем стандартный LoginView на кастомный
new_content = content.replace(
    "path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),",
    "path('login/', views.CustomLoginView.as_view(template_name='accounts/login.html'), name='login'),"
)

with open('accounts/urls.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("URL обновлен для использования кастомного LoginView!")