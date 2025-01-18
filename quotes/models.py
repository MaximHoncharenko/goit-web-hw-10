from django.db import models
from django.contrib.auth.models import User

# Модель автора
class Author(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

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
