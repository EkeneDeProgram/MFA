# Import Django module
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

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




