from django.contrib.auth.backends import BaseBackend
from map.models import Student

class StudentBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = Student.objects.get(username=username)
            if user.check_password(password):
                return user
        except Student.DoesNotExist:
            return None
    def get_user(self, user_id):
        try:
            return Student.objects.get(pk=user_id)
        except Student.DoesNotExist:
            return None
