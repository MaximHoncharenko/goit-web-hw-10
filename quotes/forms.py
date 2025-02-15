# quotes/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    """Форма реєстрації користувача"""
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

class CustomAuthenticationForm(AuthenticationForm):
    """Форма для входу користувача"""
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

from .models import Author

class AuthorForm(forms.ModelForm):
    """Форма для додавання нового автора"""
    class Meta:
        model = Author
        fields = ['fullname', 'birth_date', 'birth_place', 'description']  # Правильні поля для моделі Author
        widgets = {
            'fullname': forms.TextInput(attrs={'class': 'form-control'}),  # Ім'я автора
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),  # Дата народження
            'birth_place': forms.TextInput(attrs={'class': 'form-control'}),  # Місце народження
            'description': forms.Textarea(attrs={'class': 'form-control'}),  # Опис автора
        }

from .models import Quote



class QuoteForm(forms.ModelForm):
    """Форма для додавання нової цитати"""
    class Meta:
        model = Quote
        fields = ['quote', 'author', 'tags', 'user']  # Додано поле user
        widgets = {
            'quote': forms.Textarea(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.instance.user = user  # Заповнюємо поле користувача