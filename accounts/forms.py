from allauth.account.forms import SignupForm, LoginForm
from django.contrib.auth.models import User
from django import forms
from django.forms import widgets
from django.forms.formsets import formset_factory

from PIL import Image

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

    prefix = 'profile'

    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('choices')
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['skills'].choices = choices

    fullname = forms.CharField(max_length=255, label='')
    bio = forms.CharField(widget=forms.Textarea, label='', required=False)
    skills = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple)

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
            'skills',
        )


class CustomSkillsForm(forms.Form):
    """
    Form to capture the custom skills
    added by each user.
    """

    def __init__(self, *args, **kwargs):
        super(CustomSkillsForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = ""

    name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': 'New skill',
        }),
    )


# Define the formsets for Custom Skills
CustomSkillsFormSet = formset_factory(CustomSkillsForm)


#  Define the formsets for Custom Skills fpr Profile Portfolios (My Projects)
portfolio_inline_formset = forms.inlineformset_factory(
    User,
    models.Portfolio,
    extra=1,
    fields=('name', 'url'),
    widgets={
        'name': forms.TextInput(attrs={'placeholder': 'Project Name'}),
        'url': forms.URLInput(attrs={'placeholder': 'Project URL'},)}
)


class AvatarForm(forms.ModelForm):
    """
    Capture the user's Avatar data.
    """
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())
    rotate = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = models.Profile
        fields = (
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
        photo = super(AvatarForm, self).save()
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
        return photo
