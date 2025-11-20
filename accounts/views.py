from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .models import LoyaltyProgram
from django.contrib.auth.models import User 
from .forms import UserRegistrationForm, CustomUserCreationForm  # Добавляем новую форму
from .utils import send_registration_email
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from .models import UserProfile
from django.conf import settings
import secrets
from django.contrib.auth.views import LoginView

@csrf_exempt
def register(request):
    if request.method == 'POST':
        # Используем новую форму с дополнительными полями
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Деактивируем до подтверждения email
            user.save()

            from django.db import transaction
            with transaction.atomic():
                profile = user.userprofile
                profile.verification_token = secrets.token_urlsafe(32)
                profile.save()
                print(f"Создан токен: {profile.verification_token}")  # Для отладки
            
            # Отправка email для подтверждения
            verification_url = request.build_absolute_uri(
                f"/accounts/verify-email/{profile.verification_token}/"
            )
            
            try:
                send_mail(
                    'Подтверждение email - MebelShop',
                    f'''Здравствуйте, {user.first_name}!

Благодарим за регистрацию в MebelShop!

Для подтверждения вашего email перейдите по ссылке:
{verification_url}

Если вы не регистрировались на нашем сайте, проигнорируйте это письмо.

С уважением,
Команда MebelShop''',
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
                messages.info(request, 'Регистрация успешна! Проверьте ваш email для подтверждения.')
                return render(request, 'accounts/registration_email_sent.html')
                
            except Exception as e:
                # Если email не отправился, активируем пользователя вручную
                user.is_active = True
                user.save()
                messages.warning(request, f'Регистрация успешна, но не удалось отправить email. Ошибка: {str(e)}')
                return redirect('login')
        else:
            # Если форма невалидна, показываем ошибки
            return render(request, 'accounts/register.html', {'form': form})
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def verify_email(request, token):
    try:
        profile = UserProfile.objects.get(verification_token=token)
        user = profile.user  # Получаем самого пользователя
        user.is_active = True
        user.save()

        profile.email_verified = True
        profile.verification_token = ''
        profile.save()
        
#        from django.contrib.auth import login
#        user.backend = 'django.contrib.auth.backends.ModelBackend'
        # Автоматически логиним пользователя после подтверждения
#        login(request, user)
        messages.success(request, 'Email успешно подтвержден! Теперь вы можете войти в систему.')
        return redirect('login')
        
    except UserProfile.DoesNotExist:
        messages.error(request, 'Неверная ссылка подтверждения.')
        return render(request, 'accounts/verification_failed.html')

@login_required
def profile(request):
    loyalty, created = LoyaltyProgram.objects.get_or_create(user=request.user)
    return render(request, 'accounts/profile.html', {'loyalty': loyalty})

def test_email(request):
    """Тестовая страница для проверки отправки email"""
    # Создаем тестового пользователя
    test_user, created = CustomUser.objects.get_or_create(
        username='test_user',
        defaults={
            'email': 'test@example.com', 
            'password': 'testpass123',
            'first_name': 'Тест',
            'last_name': 'Пользователь',
            'phone': '+79999999999'
        }
    )
    
    # Тестовый URL подтверждения
    confirm_url = 'http://127.0.0.1:8000/accounts/verify-email/test-token/'
    
    # Пробуем отправить email
    try:
        send_mail(
            'Тестовое письмо - MebelShop',
            f'Это тестовое письмо. URL: {confirm_url}',
            settings.DEFAULT_FROM_EMAIL,
            [test_user.email],
            fail_silently=False,
        )
        return render(request, 'accounts/test_email.html', {
            'success': True,
            'message': '✅ Тестовое письмо успешно отправлено! Проверьте консоль сервера.'
        })
    except Exception as e:
        return render(request, 'accounts/test_email.html', {
            'success': False,
            'message': f'❌ Ошибка при отправке письма: {str(e)}'
        })
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
