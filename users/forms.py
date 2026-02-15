from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from users.models import User


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