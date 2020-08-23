from allauth.account.forms import SignupForm, LoginForm
from django.contrib.auth.models import User
from django import forms
from django.forms import widgets
from django.forms.formsets import formset_factory
from io import BytesIO as StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile

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
        {'placeholder': 'Tell us about yourself...'
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
        required=False,
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': 'New skill',
        })
    )


# Define the formset for user's Custom Skills
CustomSkillsFormSet = formset_factory(CustomSkillsForm)

#  Define the formset for user's Profile Portfolios (My Projects)
portfolio_inline_formset = forms.inlineformset_factory(
    User,
    models.Portfolio,
    extra=1,
    fields=('name', 'url'),
    widgets={
        'name': forms.TextInput(attrs={'placeholder': 'Project Name'}),
        'url': forms.URLInput(attrs={'placeholder': 'Project URL'}, )}
)


class AvatarForm(forms.ModelForm):
    """
    Capture the user's Avatar data.
    """
    x = forms.FloatField(widget=forms.HiddenInput(), required=False)
    y = forms.FloatField(widget=forms.HiddenInput(), required=False)
    width = forms.FloatField(widget=forms.HiddenInput(), required=False)
    height = forms.FloatField(widget=forms.HiddenInput(), required=False)
    rotate = forms.FloatField(widget=forms.HiddenInput(), required=False)

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
        user = super(AvatarForm, self).save()
        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')
        r = -self.cleaned_data.get('rotate')
        new_size = 400, 400

        pil_image = Image.open(user.avatar)
        rgb_im = pil_image.convert('RGB')
        rotated_image = rgb_im.rotate(r, expand=True)
        cropped_image = rotated_image.crop((x, y, w + x, h + y))
        resized_image = cropped_image.resize(new_size, Image.ANTIALIAS)
        filename = user.avatar.name
        output = StringIO()
        resized_image.save(output, format='JPEG', quality=60)
        output.seek(0)  # Change the stream position to the given byte offset.
        new_image = InMemoryUploadedFile(
            output,
            'ImageField',
            '{}.jpg'.format(filename),
            'image/jpeg',
            output.__sizeof__(),
            None,
        )
        user.avatar = new_image
        user.save()
        return user
