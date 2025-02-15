from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView


# Модель автора
class Author(models.Model):
    fullname = models.CharField(max_length=200)
    birth_date = models.DateField(null=True, blank=True)
    birth_place = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.fullname


class Quote(models.Model):
    quote = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, related_name='quotes')
    tags = models.ManyToManyField('Tag', related_name='quotes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quotes')

# Модель тегів
class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Назва тегу

    def __str__(self):
        return self.name
    

# Представлення для скидання пароля
class CustomPasswordResetView(PasswordResetView):
    template_name = "quotes/password_reset.html"

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = "quotes/password_reset_done.html"

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "quotes/password_reset_confirm.html"

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "quotes/password_reset_complete.html"
