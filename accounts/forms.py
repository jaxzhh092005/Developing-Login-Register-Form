from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from django.db import transaction

from .models import Profile

User = get_user_model()


def _input(placeholder, type_="text", **extra):
    return forms.TextInput(attrs={"placeholder": placeholder, **extra}) if type_ == "text" else \
        forms.PasswordInput(attrs={"placeholder": placeholder, **extra})


class RegisterForm(forms.Form):
    full_name = forms.CharField(max_length=150, widget=_input("Full name", autocomplete="name"))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email", "autocomplete": "email"}))
    phone = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={"placeholder": "Phone number", "autocomplete": "tel", "inputmode": "tel"}))
    password1 = forms.CharField(widget=_input("Password", "password", autocomplete="new-password"))
    password2 = forms.CharField(widget=_input("Confirm password", "password", autocomplete="new-password"))
    agree = forms.BooleanField(error_messages={"required": "You must agree to the Terms and Privacy Policy."})

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def clean(self):
        cleaned = super().clean()
        p1, p2 = cleaned.get("password1"), cleaned.get("password2")
        if p1 and p2:
            if p1 != p2:
                self.add_error("password2", "Passwords do not match.")
            else:
                try:
                    validate_password(p1)
                except forms.ValidationError as e:
                    self.add_error("password1", e)
        return cleaned

    @transaction.atomic
    def save(self):
        d = self.cleaned_data
        first, _, last = d["full_name"].strip().partition(" ")
        user = User.objects.create_user(
            username=d["email"], email=d["email"], password=d["password1"],
            first_name=first, last_name=last,
        )
        Profile.objects.create(user=user, phone=d["phone"])
        # AUTHORIZATION: every new account starts with the lowest role
        member, _ = Group.objects.get_or_create(name="Member")
        user.groups.add(member)
        return user


class EmailLoginForm(AuthenticationForm):
    """AUTHENTICATION: log in with email + password (case-insensitive email)."""
    username = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "Email or username", "autocomplete": "username", "autofocus": True}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={"placeholder": "Password", "autocomplete": "current-password"}))

    def clean_username(self):
        u = self.cleaned_data["username"].strip()
        return u.lower() if "@" in u else u
