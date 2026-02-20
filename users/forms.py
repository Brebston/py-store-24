from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from users.models import Address, User

from phonenumber_field.formfields import PhoneNumberField


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            "class": "input",
            "placeholder": "Alex",
        })
    )

    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            "class": "input",
            "placeholder": "Johnson"
        })
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
        "class": "input",
        "placeholder": "user@email.com"
        })
    )

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            "class": "input",
            "placeholder": "Minimum 8 characters"
        })
    )

    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            "class": "input",
            "placeholder": "Repeat password"
        })
    )


class LoginForm(AuthenticationForm):

    username = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            "class": "input",
            "placeholder": "user@email.com"
        })
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            "class": "input",
            "placeholder": "••••••••"
        })
    )


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone",
            "notes",
        )

    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "input",
            "placeholder": "Alex",
        })
    )

    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "input",
            "placeholder": "Johnson"
        })
    )

    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            "class": "input",
            "placeholder": "user@email.com"
        })
    )

    phone = PhoneNumberField(
        region="PL",
        required=False,
        widget=forms.TextInput(attrs={
            "class": "input",
            "placeholder": "+1 555 123 456"
        })
    )

    notes = forms.CharField(
        required=False,
        label="Order notes (optional)",
        widget=forms.Textarea(attrs={
            "class": "input",
            "placeholder": "Delivery instructions, gate code, etc."
        })
    )
