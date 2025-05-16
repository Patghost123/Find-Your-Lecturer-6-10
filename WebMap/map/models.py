from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.contrib.auth.hashers import make_password
from django.utils.text import slugify

class StudentManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(username=username, email=email)
        user.set_password(password)  # Secure password hashing
        user.is_staff = False  # Prevent normal users from accessing admin
        user.is_active = True  # Needed for authentication
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username, email, password)
        user.is_staff = True  # Allows admin panel access
        user.is_superuser = True  # Grants full permissions
        user.save(using=self._db)
        return user

class Student(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    is_staff = models.BooleanField(default=False)  # Required for admin access
    is_active = models.BooleanField(default=True)  # Needed for authentication

    objects = StudentManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

class Lecturer(models.Model):
    name = models.CharField(max_length=255,)
    slug = models.SlugField(unique=True, blank=True)
    position = models.CharField(max_length=255, blank=True)
    faculty = models.CharField(max_length=255, blank=True)
    room_number = models.CharField(max_length=50, blank=True)  
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    profile_url = models.URLField(blank=True)
    office_hours = models.TextField()
    profile_pic = models.ImageField(upload_to='lecturer_profiles/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name