from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class LoginForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'nickname', 'password1', 'password2',)


