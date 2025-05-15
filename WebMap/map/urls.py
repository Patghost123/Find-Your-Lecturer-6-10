from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from map.views import students_list
from django.conf import settings
from django.conf.urls.static import static
from .views import get_lecturers, lecturer_profile

urlpatterns = [
    path('', views.home, name="home"),
    path('join/', views.join, name="join"),
    path('login/', views.login, name="login"),
    path('home/', views.home, name="home"),
    path('success/', views.success, name="success"),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path("students/", views.students_list, name="students_list"),
    path('map/<int:floor_number>/', views.floor_map, name='floor_map'),
    path("get_lecturers/", views.get_lecturers, name="get_lecturers"),
    path("lecturer/<str:lecturer_name>/", views.lecturer_profile, name="lecturer_profile"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
