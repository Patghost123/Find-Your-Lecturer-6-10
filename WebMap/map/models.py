from django.db import models


class Student(models.Model):
    email = models.EmailField(max_length=200)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    
    def __str__(self):
        return self.username

def set_password(self, raw_password):
        self.password = make_password(raw_password)

def check_password(self, raw_password):
        return check_password(raw_password, self.password)