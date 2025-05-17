from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models
from django.contrib.auth.hashers import make_password
from django.utils.text import slugify

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, role='student'):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(username=username, email=email, role=role)
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username, email, password, role='admin')
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('lecturer', 'Lecturer'),
        ('admin', 'Admin'),
    )

    username = models.CharField(unique=True, max_length=100)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.username} ({self.role})"

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

class Lecturer(models.Model):
    name = models.CharField(max_length=255,)
    slug = models.SlugField(unique=True, blank=True)
    position = models.CharField(max_length=255, blank=True)
    faculty = models.CharField(max_length=255, blank=True)
    room_number = models.CharField(max_length=50, null=True, blank=True)  
    phone = models.CharField(max_length=50, null=True, blank=True)
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