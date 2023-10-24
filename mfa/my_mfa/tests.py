from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import UserProfile 



# Create your tests here.
class RegistrationIntegrationTest(TestCase):
    def test_register_user_with_valid_data(self):
        # Define the URL for the registration view
        url = reverse("registration")

        # Simulate a POST request with valid data
        response = self.client.post(url, {
            "username": "Bruno",
            "email": "Bruno@gmail.com",
            "password1": "mSAEsE3NzdFu3nK!",
            "password2": "mSAEsE3NzdFu3nK!",
        })

        # Check that the user is redirected to the index page after successful registration
        self.assertRedirects(response, reverse("index"))

        # Check that the user is now logged in
        self.assertTrue(response.wsgi_request.user.is_authenticated)

        # Verify that the user was created in the database
        user = User.objects.get(username="Bruno")
        self.assertIsNotNone(user)

    def test_register_user_with_invalid_data(self):
        # Define the URL for the registration view
        url = reverse("registration")

        # Simulate a POST request with invalid data
        response = self.client.post(url, {
            'username': "DeBruyne",
            'email': "DeB@g",  # Invalid email format
            'password1': "weakWord",  # Password doesn't meet requirements
            'password2': "mismatchword",  # Passwords don't match
        })

        # Check that the form is not valid and the user is not registered
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertFalse(User.objects.filter(username="DeBruyne").exists())



