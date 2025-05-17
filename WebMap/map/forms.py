from django import forms
from .models import CustomUser

class userForm(forms.ModelForm):
    
    class Meta:
        model = CustomUser
        fields = ["email", "username" , "password"]
