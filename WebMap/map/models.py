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

    def create_superuser(self, email, username, password=None):
        student = self.create_user(email, username, password)
        student.is_staff = True
        student.is_superuser = True
        student.save(using=self._db)
        return student

class Student(AbstractBaseUser):
    email = models.EmailField(max_length=200, unique=True)
    username = models.CharField(max_length=100, unique=True)
    
    # Use Django’s built-in password handling
    password = models.CharField(max_length=128)  # Stored securely via set_password()
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = StudentManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username