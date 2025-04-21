from django import forms
from .models import Student

class userForm(forms.ModelForm):
    
    class Meta:
        model = Student
        fields = ["email", "username" , "passwd"]
