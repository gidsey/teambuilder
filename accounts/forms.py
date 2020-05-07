from django import forms

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


# ---Signup form
class SignUpForm(UserCreationForm):
    """Define the SignUpForm which extends UserCreationForm"""
    email = forms.EmailField(required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
    email.widget.attrs.update({'placeholder': 'Email Address'})

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            'email',
            'password1',
            'password2',
        )
