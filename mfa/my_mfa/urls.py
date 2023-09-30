from django.urls import path
from . import views


urlpatterns = [
    path("registration/", views.register_user, name="registration"),
    path("authentication/", views.user_authentication, name="authentication"),
    path("mfa-status/", views.mfa_status, name="mfa_status"),
    path("mfa-verification/", views.mfa_verification, name="mfa_verification"),
]