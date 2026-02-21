from django.urls import path, reverse_lazy
from django.contrib.auth.views import LogoutView

from users.views import (
    AccountView,
    AddressCreateView,
    AddressDeleteView,
    AddressListView,
    AddressUpdateView,
    UserLoginView,
    RegisterView,
    set_default_address,
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
    path("addresses/", AddressListView.as_view(), name="address_list"),
    path("addresses/add/", AddressCreateView.as_view(), name="address_add"),
    path("addresses/<int:pk>/edit/", AddressUpdateView.as_view(), name="address_edit"),
    path("addresses/<int:pk>/delete/", AddressDeleteView.as_view(), name="address_delete"),
    path("addresses/<int:pk>/default/", set_default_address, name="address_default"),
]
