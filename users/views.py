from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView
from django.contrib import messages

from users.forms import LoginForm, ProfileUpdateForm, RegisterForm
from users.mixins.mixins import AnonymousRequiredMixin


class AccountView(LoginRequiredMixin, View):
    template_name = "users/profile.html"

    def get(self, request):
        context = {
            "profile_form":  ProfileUpdateForm(
                instance=request.user,
                prefix="profile"
            ),
        }
        return render(request, self.template_name, context)

    def post(self, request):
        profile_form = ProfileUpdateForm(
            request.POST,
            instance=request.user,
            prefix="profile"
        )

        if "profile-submit" in request.POST:
            if profile_form.is_valid():
                profile = profile_form.save(commit=False)
                profile.user = request.user
                profile.save()
                messages.success(request, "Profile updated successfully!")
                return redirect("users:profile")

        context = {
            "profile_form": profile_form,
        }

        return render(request, self.template_name, context)


class UserLoginView(AnonymousRequiredMixin, LoginView):
    template_name = "users/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True


class RegisterView(AnonymousRequiredMixin, CreateView):
    form_class = RegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:profile")
