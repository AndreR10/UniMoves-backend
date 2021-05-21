from django.urls import path, include
from .views import BlacklistTokenUpdateView
from dj_rest_auth.registration.views import VerifyEmailView, ConfirmEmailView
from rest_framework import urlpatterns
from django.db import router
from rest_framework.routers import DefaultRouter
from .views import UserView, UserEditView, UserProfileView

router = DefaultRouter()
router.register("my-profile/edit", UserEditView, basename="profile-edit")
router.register("my-profile/detail", UserView, basename="profile-detail")
router.register("users", UserProfileView, basename="users")

urlpatterns = [
     path("registration/account-confirm-email/<str:key>/",
         ConfirmEmailView.as_view()),
     path("", include("dj_rest_auth.urls")),
     path("login/", include("dj_rest_auth.urls")),
     path("logout/blacklist/",
          BlacklistTokenUpdateView.as_view(),
          name="blacklist"),
     path("registration/", include("dj_rest_auth.registration.urls")),
     path("account-confirm-email/", VerifyEmailView.as_view()),
]

urlpatterns += router.urls