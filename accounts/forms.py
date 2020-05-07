from django import forms

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


# ---Signup form
class SignUpForm(UserCreationForm):
    """Define the SignUpForm which extends UserCreationForm"""
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            'email',
            'password1',
            'password2',
        )
