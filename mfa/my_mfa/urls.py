from django.urls import path
from . import views


urlpatterns = [
    path("registration/", views.register_user, name="registration"),
    path("mfa/", views.enable_mfa, name="mfa"),
    path("mfa-method/", views.set_mfa_method, name="mfa-method"),
    path("mfa_settings/", views.update_mfa_status, name="mfa_settings"),
    path("mfa-verification/", views.mfa_verification, name="mfa_verification"),
]