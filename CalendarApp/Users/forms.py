from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm): # New form that inherits from the UserCreationForm class
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()  
    class Meta:
        model = User
        fields = ['username', 'email'] # Create a form that only lets the user change his/her usename and email
