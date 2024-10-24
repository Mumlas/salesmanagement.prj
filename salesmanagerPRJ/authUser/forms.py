from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('phone_number','name','privileges')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('phone_number','name','privileges')