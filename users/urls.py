from django.urls import path, reverse_lazy
from django.contrib.auth.views import LogoutView

from users.views import (
    AccountView,
    UserLoginView,
    RegisterView,
)

app_name = "users"

urlpatterns = [
    path("profile/", AccountView.as_view(), name="profile"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path(
        "logout/",
         LogoutView.as_view(next_page=reverse_lazy("core:index")),
         name="logout"
         ),
]
