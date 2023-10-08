from django.urls import path
from . import views


urlpatterns = [
    path("registration/", views.register_user, name="registration"),
    path("mfa/", views.enable_mfa, name="mfa"),
    path("mfa-method/", views.set_mfa_method, name="mfa-method"),
    path("login/", views.user_authentication, name="login"),
    path("totp-qr-code", views.generate_totp_qr_code, name="totp-qr-code"),
    path("mfa_settings/", views.update_mfa_status, name="mfa_settings"),
]