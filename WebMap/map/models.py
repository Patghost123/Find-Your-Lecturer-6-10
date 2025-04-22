from django.db import models


class Student(models.Model):
    email = models.EmailField(max_length=200)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    
    def __str__(self):
        return self.username