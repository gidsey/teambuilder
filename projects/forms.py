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

    title.widget.attrs.update({
        'class': 'circle--input--h1',
        'placeholder': 'Project Title',
    })

    description.widget.attrs.update({
        'class': 'generic-textarea',
        'placeholder': 'Project description...'
    })

    timeline.widget.attrs.update({
        'class': 'circle--textarea--input',
        'placeholder': 'Time estimate',
    })

    requirements.widget.attrs.update({
        'class': 'circle--textarea--input',
    })


#  Define the formset for Positions attached to a Project
position_inline_formset = forms.inlineformset_factory(
    models.Project,
    models.Position,
    extra=1,
    fields=('title', 'description'),
    widgets={
        'title': forms.TextInput(attrs={'placeholder': 'Position Title', 'class': 'circle--input--h3'}),
        'description': forms.Textarea(attrs={'placeholder': 'Position description...'},)}
)


class DeleteProjectForm(forms.Form):
    class Meta:
        fields = ('title',)
