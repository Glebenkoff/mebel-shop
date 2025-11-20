from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'middle_name', 'phone', 'email', 'address']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'middle_name': 'Отчество',
            'phone': 'Телефон',
            'email': 'Email',
            'address': 'Адрес доставки',
        }
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }