from django.urls import path, include
from . import views
from .views import join, login, hello

urlpatterns = [
    path('', views.hello, name="hello"),
    path('join/', views.join, name="join"),
    path('login/', views.login, name="login"),
    path('hello/', views.hello, name="hello"),
    path('success/', views.success, name = "success"),
] 