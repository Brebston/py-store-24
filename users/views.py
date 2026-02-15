from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from users.forms import RegisterForm


class AccountView(LoginRequiredMixin, TemplateView):
    template_name = "users/account.html"


class UserLoginView(LoginView):
    template_name = "users/login.html"


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:account")
