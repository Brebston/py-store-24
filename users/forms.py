from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm

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


class ProfileAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "street",
            "postal_code",
            "city",
            "state",
            "country",
            "notes",
            "is_default",
        ]

        widgets = {
            "first_name": forms.TextInput(attrs={
                "class": "input",
                "placeholder": "John"
            }),
            "last_name": forms.TextInput(attrs={
                "class": "input",
                "placeholder": "Doe"
            }),
            "email": forms.EmailInput(attrs={
                "class": "input",
                "placeholder": "john@example.com"
            }),
            "phone": forms.TextInput(attrs={
                "class": "input",
                "placeholder": "+48 123 456 789"
            }),
            "street": forms.TextInput(attrs={
                "class": "input",
                "placeholder": "Street name 123"
            }),
            "postal_code": forms.TextInput(attrs={
                "class": "input",
                "placeholder": "00-000"
            }),
            "city": forms.TextInput(attrs={
                "class": "input",
                "placeholder": "Warsaw"
            }),
            "state": forms.TextInput(attrs={
                "class": "input",
                "placeholder": "Mazowieckie"
            }),
            "country": forms.TextInput(attrs={
                "class": "input",
                "placeholder": "Poland"
            }),
            "notes": forms.Textarea(attrs={
                "class": "input",
                "placeholder": "Floor, door code, delivery instructions...",
                "rows": 3
            }),
            "is_default": forms.CheckboxInput(attrs={
                "style": "width:18px;height:18px;cursor:pointer;"
            }),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get("phone", "")
        phone = phone.strip()
        return phone

    def clean_postal_code(self):
        postal = self.cleaned_data.get("postal_code", "")
        return postal.strip()


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["old_password"].widget = forms.PasswordInput(attrs={
            "autocomplete": "current-password",
            "placeholder": "••••••••",
            "class": "input"
        })

        self.fields["new_password1"].widget = forms.PasswordInput(attrs={
            "autocomplete": "new-password",
            "placeholder": "Min 8 characters",
            "class": "input"

        })
        self.fields["new_password1"].label = "New password"

        self.fields["new_password2"].widget = forms.PasswordInput(attrs={
            "autocomplete": "new-password",
            "placeholder": "Repeat new password",
            "class": "input"
        })
        self.fields["new_password2"].label = "Repeat new password"
