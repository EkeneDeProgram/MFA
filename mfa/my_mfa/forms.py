# Import Django module
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):

  class Meta:
        model = User  # Set your custom User model if you have one
        fields = ('username', 'email', 'password1', 'password2')




