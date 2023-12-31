# Import Django modules
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
# Create a user profile model to store mfa-related informations.  
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mfa_enabled = models.BooleanField(default=False)
    mfa_method = models.CharField(max_length=4, choices=[("TOTP", "TOTP"), ("SMS", "SMS")])
    totp_secret_key = models.CharField(max_length=200, unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True, help_text="Enter your phone number in the format: +2348155813450")
    encryption_key = models.CharField(max_length=200, null=True, blank=False)
    name = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to="media/qr_codes/", null=True, blank=True)
   
