from django.db import models
from django.contrib.auth.models import User

# Create your models here.
 # Create a separate user profile model to store additional Client-related data, including MFA settings  
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    secret_key = models.CharField(max_length=200, unique=True, null=True, blank=True)
    mfa_enabled = models.BooleanField(default=False)
    phone_number = models.CharField(
        max_length=13, 
        unique=True, 
        null=True, 
        blank=True,
        help_text="Enter your phone number in the format: +2348155813450"
    )
