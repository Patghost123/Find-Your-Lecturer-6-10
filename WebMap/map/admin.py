from django.contrib import admin
from map.models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ["username", "is_superuser", "is_staff"]
