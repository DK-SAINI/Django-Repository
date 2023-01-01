from django.urls import path

from authentication.views import (
    UserRegistrationView,
    SendOtpEmailVerifyView,
    EmailVerifyView,
    UserLogInView,
    UserLogOutView,
    UserChangePasswordView,
    ForgotPasswordView,
    ConfirmForgotPasswordView,
    UserDetailView,
)


urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path(
        "email_verify_otp/",
        SendOtpEmailVerifyView.as_view(),
        name="email_verify_otp",
    ),
    path("email_verify/", EmailVerifyView.as_view(), name="email_verify"),
    path("login/", UserLogInView.as_view(), name="login"),
    path("logout/", UserLogOutView.as_view(), name="logout"),
    path(
        "change_password/",
        UserChangePasswordView.as_view(),
        name="change_password",
    ),
    path(
        "forgot_password/",
        ForgotPasswordView.as_view(),
        name="forgot_password",
    ),
    path(
        "confirm_forgot_password/",
        ConfirmForgotPasswordView.as_view(),
        name="confirm_forgot_password",
    ),
    path("user/", UserDetailView.as_view(), name="user"),
]
