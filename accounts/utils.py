from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_registration_email(user, confirm_url):
    """Отправка email для подтверждения регистрации"""
    subject = 'Подтверждение регистрации - MebelShop'
    
    context = {
        'username': user.username,
        'confirm_url': confirm_url,
    }
    
    html_content = render_to_string('emails/registration_confirm.html', context)
    text_content = strip_tags(html_content)
    
    try:
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
        return True
    except Exception as e:
        print(f"Ошибка отправки email: {e}")
        return False

def send_order_confirmation(user, order, order_items):
    """Отправка email о создании заказа"""
    subject = f'Заказ #{order.id} создан - MebelShop'
    
    context = {
        'username': user.username,
        'order': order,
        'order_items': order_items,
        'order_url': f'{settings.SITE_URL}/orders/{order.id}/'
    }
    
    html_content = render_to_string('emails/order_created.html', context)
    text_content = strip_tags(html_content)
    
    try:
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
        return True
    except Exception as e:
        print(f"Ошибка отправки email: {e}")
        return False

def send_password_reset_email(user, reset_url):
    """Отправка email для сброса пароля"""
    subject = 'Восстановление пароля - MebelShop'
    
    context = {
        'username': user.username,
        'reset_url': reset_url,
    }
    
    html_content = render_to_string('emails/password_reset.html', context)
    text_content = strip_tags(html_content)
    
    try:
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
        return True
    except Exception as e:
        print(f"Ошибка отправки email: {e}")
        return False