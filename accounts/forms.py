from allauth.account.forms import SignupForm
from django.forms import widgets


class CustomSignUpForm(SignupForm):
    """
    Customise the placeholder text on the SignUpForm,
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

