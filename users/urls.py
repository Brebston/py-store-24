from django.urls import path

from users.views import (
    AccountView,
    LoginView,
    RegisterView,
)

app_name = "users"

urlpatterns = [
    path("account/", AccountView.as_view(), name="account"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
]
