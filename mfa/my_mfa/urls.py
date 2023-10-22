from django.urls import path
from . import views


urlpatterns = [
    path("registration/", views.register_user, name="registration"),
    path("login/", views.user_authentication, name="login"),
    path("totp-qr-code/", views.generate_totp_qr_code, name="totp-qr-code"),
    path("verify-totp/", views.verify_totp, name="verify-totp"),
    path("check_email_availability/", views.check_email_availability, name="check_email_availability"),
]