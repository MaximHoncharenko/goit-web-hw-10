from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('tag/<str:tag>/', views.quotes_by_tag, name='quotes_by_tag'),
    path('register/', views.register, name='register'),  # Сторінка реєстрації
    path('user_login/', views.user_login, name='login'),      # Сторінка входу
    path('user_logout/', views.user_logout, name='logout'),   # Сторінка виходу
    path('add-author/', views.add_author, name='add_author'),  # Додавання автора
    path('add-quote/', views.add_quote, name='add_quote'),     # Додавання цитати
    path('author/<str:author_id>/', views.author_detail, name='author_detail'),
    ]