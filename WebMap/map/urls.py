from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from map.views import students_list

urlpatterns = [
    path('', views.home, name="home"),
    path('join/', views.join, name="join"),
    path('login/', views.login, name="login"),
    path('home/', views.home, name="home"),
    path('success/', views.success, name="success"),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path("students/", views.students_list, name="students_list"),
]