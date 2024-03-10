from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from django_rest_passwordreset.views import (
    reset_password_request_token,
    reset_password_validate_token,
)

from .views import (
    CustomTokenObtainPairView,
    RegisterView,
    ProfileView,
    LogoutAPIView,
    ChangePasswordView,
    DeactivateAccountView,
    PasswordResetConfirmAPIView,
)

app_name = "authx"

urlpatterns = [
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", RegisterView.as_view(), name="authx_register"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path(
        "change_password/<int:pk>/",
        ChangePasswordView.as_view(),
        name="change_password",
    ),
    path("password_reset/", reset_password_request_token, name="password_reset"),
    path(
        "password_reset/validate_token/",
        reset_password_validate_token,
        name="password_reset_validate_token",
    ),
    path(
        "password_reset/confirm/",
        PasswordResetConfirmAPIView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "deactivate-account/",
        DeactivateAccountView.as_view(),
        name="deactivate-account",
    ),
]
