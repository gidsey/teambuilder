from allauth.account.forms import SignupForm, LoginForm
from django.forms import widgets
from django import forms

from . import models


class CustomSignUpForm(SignupForm):
    """
    Customise the placeholder text on the SignUp form,
    extending the django allauth form.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].widget = widgets.TextInput(
            attrs={
                'placeholder': 'Email Address',
            })

        self.fields['password1'].widget = widgets.PasswordInput(
            attrs={
                'placeholder': 'Password',
            })

        self.fields['password2'].widget = widgets.PasswordInput(
            attrs={
                'placeholder': 'Confirm Password',
            })


class CustomLoginForm(LoginForm):
    """
    Customise the placeholder text on the Login form,
    extending the django allauth form.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['login'].widget = widgets.TextInput(
            attrs={
                'placeholder': 'Email Address',
            })


class ProfileForm(forms.ModelForm):
    """
    Define the Profile Form.
    """
    fullname = forms.CharField(max_length=255)
    bio = forms.CharField(widget=forms.Textarea, required=False)

    fullname.widget.attrs.update({
        'class': 'circle--input--h1',
        'placeholder': 'Full Name',
    })

    bio.widget.attrs.update(
        {'class': 'teambuilder_textarea',
         'placeholder': 'Tell us about yourself...'
    })

    class Meta:
        model = models.Profile
        fields = (
            'fullname',
            'bio',
        )
