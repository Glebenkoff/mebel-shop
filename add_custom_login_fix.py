# add_custom_login_fix.py
custom_login_code = '''
from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    
    def form_valid(self, form):
        # Проверяем checkbox "Запомнить меня"
        remember_me = self.request.POST.get('remember_me')
        print(f"Remember me: {remember_me}")  # Для отладки
        
        if remember_me:
            # Устанавливаем длительную сессию (2 недели)
            self.request.session.set_expiry(1209600)  # 2 недели в секундах
        else:
            # Сессия до закрытия браузера
            self.request.session.set_expiry(0)
            
        return super().form_valid(form)
'''

# Читаем текущий файл
with open('accounts/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Добавляем импорт если его нет
if 'from django.contrib.auth.views import LoginView' not in content:
    # Добавляем в начало после других импортов
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'from django' in line or 'import' in line:
            continue
        else:
            # Вставляем после импортов
            lines.insert(i, 'from django.contrib.auth.views import LoginView')
            break
    content = '\n'.join(lines)

# Добавляем класс в конец файла
if 'class CustomLoginView' not in content:
    content += custom_login_code

with open('accounts/views.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("CustomLoginView добавлен в views.py!")