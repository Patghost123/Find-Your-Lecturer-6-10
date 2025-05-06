from django.urls import path, include
from . import views
from .views import join, login, hello, login_check
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.hello, name="hello"),
    path('join/', views.join, name="join"),
    path('login/', views.login, name="login"),
    path('hello/', views.hello, name="hello"),
    path('success/', views.success, name = "success"),
    path('logout/', auth_views.LogoutView.as_view(next_page='hello'), name='logout'),
    path('login/submit/', login, name='login'),
    path('login/check/', login_check, name='login_check'),
] 