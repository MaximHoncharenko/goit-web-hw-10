from django.urls import path
from django.contrib.auth import views as auth_views  # Імпортуємо вбудовані перегляди

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
    
    # URL для скидання паролю
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('reset_password_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
