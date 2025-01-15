from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('tag/<str:tag>/', views.quotes_by_tag, name='quotes_by_tag'),
]