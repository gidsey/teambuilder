from django import forms
from PIL import Image

from allauth.account.forms import SignupForm, LoginForm
from django.forms import widgets


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
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())
    rotate = forms.FloatField(widget=forms.HiddenInput())

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
            'avatar',
            'x',
            'y',
            'width',
            'height',
            'rotate'
        )
        labels = {
            'avatar': '',
        }
        widgets = {
            'avatar': forms.FileInput(attrs={
                'accept': 'image/*'
            })


        }

    def save(self):
        photo = super(ProfileForm, self).save()
        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')
        r = self.cleaned_data.get('rotate')

        r = -r  # swap negative to positive and vise versa

        image = Image.open(photo.avatar)
        rotated_image = image.rotate(r, expand=True)
        cropped_image = rotated_image.crop((x, y, w + x, h + y))
        resized_image = cropped_image.resize((400, 400), Image.ANTIALIAS)
        resized_image.save(photo.avatar.path)
        print(photo.avatar)
        return photo


# class AvatarForm(forms.ModelForm):
#     """
#     Define the Avatar Form.
#     """
#     x = forms.FloatField(widget=forms.HiddenInput())
#     y = forms.FloatField(widget=forms.HiddenInput())
#     width = forms.FloatField(widget=forms.HiddenInput())
#     height = forms.FloatField(widget=forms.HiddenInput())
#     rotate = forms.FloatField(widget=forms.HiddenInput())
#
#     class Meta:
#         model = models.Profile
#         fields = ('avatar', 'x', 'y', 'width', 'height', 'rotate')
#         labels = {'avatar': '', }
#         widgets = {
#             'avatar': forms.FileInput(attrs={
#                 'accept': 'image/*'
#             })
#         }
#
#     def save(self):
#         photo = super(AvatarForm, self).save()
#         x = self.cleaned_data.get('x')
#         y = self.cleaned_data.get('y')
#         w = self.cleaned_data.get('width')
#         h = self.cleaned_data.get('height')
#         r = self.cleaned_data.get('rotate')
#
#         r = -r  # swap negative to positive and vise versa
#
#         image = Image.open(photo.avatar)
#         rotated_image = image.rotate(r, expand=True)
#         cropped_image = rotated_image.crop((x, y, w + x, h + y))
#         resized_image = cropped_image.resize((400, 400), Image.ANTIALIAS)
#         resized_image.save(photo.avatar.path)
#         print(photo.avatar)
#         return photo
