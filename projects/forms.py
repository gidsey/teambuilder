from django import forms

from . import models


class ProjectForm(forms.ModelForm):
    """
    Define the Profile Form
    """

    prefix = 'profile'

    title = forms.CharField(max_length=255, label='')
    description = forms.CharField(widget=forms.Textarea, label='', required=False)
    timeline = forms.CharField(widget=forms.Textarea, label='', required=False)
    requirements = forms.CharField(widget=forms.Textarea, label='', required=False)

    class Meta:
        model = models.Project
        fields = (
            'title',
            'description',
            'timeline',
            'requirements'
        )