# Import Django module
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class RegistrationForm(UserCreationForm):
  email = forms.EmailField(required=True)

  class Meta:
        model = User  # Set your custom User model if you have one
        fields = ('username', 'email', 'password1', 'password2')
        

  def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already associated with an account.")
        return email

  def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if (
            not any(char.islower() for char in password1) or
            not any(char.isupper() for char in password1) or
            not any(char.isdigit() for char in password1) or
            not any(char in "!@#$%^&*()_+[]{}|\\;:'\"<>,.?/~`" for char in password1)
        ):
            raise forms.ValidationError(
                "Password must contain at least one lowercase letter, one uppercase letter, one digit, and one special character."
            )
        return password1




