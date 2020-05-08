from allauth.account.forms import SignupForm, LoginForm
from django.forms import widgets


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

