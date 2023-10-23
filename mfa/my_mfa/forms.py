# Import Django module
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


class RegistrationForm(UserCreationForm):
  # Add field to the form, which are required for registration
  username = forms.CharField(max_length=40, required=True)
  email = forms.EmailField(required=True)
  password1 = forms.CharField(widget=forms.PasswordInput, required=True, label="Password")
  password2 = forms.CharField(widget=forms.PasswordInput, required=True, label="Confirm Password")


  class Meta:
        model = User  # Specify the model that the UserForm is associated with
        # Specify the fields from the User model to include in the form
        fields = ('username', 'email', 'password1', 'password2')
        
  # Check if an email address is not already associated with an existing account
  def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already associated with an account.")
        return email

 # Check if the password meets minimum requirements
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




