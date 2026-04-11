from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['username'].help_text = "Create a unique username for your account."
        self.fields['password1'].help_text = "Create a strong password "
        self.fields['password2'].help_text = "Re-enter the password for confirmation."


class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       
        self.fields['username'].help_text = "Enter your Nexus username"


