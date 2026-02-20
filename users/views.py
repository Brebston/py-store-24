from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.contrib import messages

from users.forms import LoginForm, ProfileAddressForm, ProfileUpdateForm, RegisterForm
from users.mixins.mixins import AnonymousRequiredMixin
from users.models import Address


class AccountView(LoginRequiredMixin, View):
    template_name = "users/profile.html"

    def get(self, request):
        address = request.user.addresses.first()
        context = {
            "profile_form": ProfileUpdateForm(
                instance=request.user,
                prefix="profile"
            ),

            "address_form": ProfileAddressForm(
                instance=address,
                prefix="address"
            )
        }
        return render(request, self.template_name, context)

    def post(self, request):
        address = request.user.addresses.first()
        profile_form = ProfileUpdateForm(
            request.POST,
            instance=request.user,
            prefix="profile"
        )

        address_form = ProfileAddressForm(
            request.POST,
            instance=address,
            prefix="address"
        )

        if "profile-submit" in request.POST:
            if profile_form.is_valid():
                profile = profile_form.save(commit=False)
                profile.user = request.user
                profile.save()
                messages.success(request, "Profile updated successfully!")
                return redirect("users:profile")

        if "address-submit" in request.POST:
            if address_form.is_valid():
                address = address_form.save(commit=False)
                address.user = request.user
                address.save()
                messages.success(request, "Address updated successfully!")
                return redirect("users:profile")

        context = {
            "profile_form": profile_form,
            "address_form": address_form,
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


class AddressListView(LoginRequiredMixin, ListView):
    model = Address
    template_name = "users/address_list.html"
    context_object_name = "addresses"

    def get_queryset(self):
        return self.request.user.addresses.all()


class AddressCreateView(LoginRequiredMixin, CreateView):
    model = Address
    form_class = ProfileAddressForm
    template_name = "users/address_form.html"
    success_url = reverse_lazy("users:profile")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AddressUpdateView(LoginRequiredMixin, UpdateView):
    model = Address
    form_class = ProfileAddressForm
    template_name = "users/address_form.html"
    success_url = reverse_lazy("users:profile")

    def get_queryset(self):
        return self.request.user.addresses.all()


class AddressDeleteView(LoginRequiredMixin, DeleteView):
    model = Address
    template_name = "users/address_confirm_delete.html"
    success_url = reverse_lazy("users:profile")

    def get_queryset(self):
        return self.request.user.addresses.all()


@login_required
def set_default_address(request, pk):
    address = get_object_or_404(
        Address,
        pk=pk,
        user=request.user
    )

    address.is_default = True
    address.save()

    return redirect("users:profile")