from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),  # Головна сторінка
    path('tag/<str:tag>/', views.quotes_by_tag, name='quotes_by_tag'),  # Пошук за тегом
]
