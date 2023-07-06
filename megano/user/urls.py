from django.urls import path
from .views import (
    SignUpView,
    SignOutView,
    SignInView,
    ProfileDetail,
    AvatarUpdateView,
    PasswordUpdateView,
)


urlpatterns = [
    path("sign-in", SignInView.as_view(), name="sign-in"),
    path("sign-up", SignUpView.as_view(), name="sign-up"),
    path("sign-out", SignOutView.as_view(), name="sign-out"),
    path("profile", ProfileDetail.as_view(), name="profile"),
    path("profile/password", PasswordUpdateView.as_view(), name="profilePassword"),
    path("profile/avatar", AvatarUpdateView.as_view(), name="avatar"),
]
