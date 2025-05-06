from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from map.views import custom_map


urlpatterns = [
    path('', views.hello, name="hello"),
    path('join/', views.join, name="join"),
    path('login/', views.login, name="login"),
    path('hello/', views.hello, name="hello"),
    path('success/', views.success, name="success"),
    path('logout/', auth_views.LogoutView.as_view(next_page='hello'), name='logout'),
    path('login/check/', views.login_check, name='login_check'),
    path('map/', custom_map, name='custom_map'),
]