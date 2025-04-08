from django import forms
from .models import user

class userForm(forms.ModelForm):
    
    class Meta:
        model = user
        fields = ["email", "username" , "passwd"]
