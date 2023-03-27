from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


INPUT_CLASS = 'w-full my-4 py-4 px-6 rounded-xl bg-gray-100'


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username','password',)


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','email','password1','password2',)