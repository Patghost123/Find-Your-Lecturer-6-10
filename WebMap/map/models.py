from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class StudentManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Email is required")
        student = self.model(email=email, username=username)
        student.set_password(password)  # Hash password before saving
        student.save(using=self._db)
        return student

    def create_superuser(self, username, email, password=None):
        student = self.create_user(email=email, username=username, password=password)
        student.is_staff = True
        student.is_superuser = True
        student.is_active = True  # Ensure the superuser is active
        student.save(using=self._db)
        return student

class Student(AbstractBaseUser):
    email = models.EmailField(max_length=200, unique=True)
    username = models.CharField(max_length=100, unique=True)
    
    # Password is handled by AbstractBaseUser, no need to define it again
    # password = models.CharField(max_length=128)  # Remove this line

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = StudentManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

class StudentBackend():
    def authenticate(self, request, username=None, password=None):
        try:
            user = Student.objects.get(username=username)
            if user.check_password(password) and user.is_staff:  # Ensure staff users can log in
                return user
        except Student.DoesNotExist:
            return None



    
