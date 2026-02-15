from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView

from users.forms import LoginForm, RegisterForm
from users.mixins.mixins import AnonymousRequiredMixin


class AccountView(LoginRequiredMixin, TemplateView):
    template_name = "users/account.html"


class UserLoginView(AnonymousRequiredMixin, LoginView):
    template_name = "users/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True


class RegisterView(AnonymousRequiredMixin, CreateView):
    form_class = RegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:account")
