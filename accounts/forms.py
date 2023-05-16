from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserInfo


class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ('username',  'email', 'password1', 'password2', )

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ('photo', 'phone', 'about')


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput()) # attrs={'class': 'form-control'}
    password = forms.CharField(widget=forms.PasswordInput()) # attrs={'class': 'form-control'}

