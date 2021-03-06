from django import forms

from . import models


class ProjectForm(forms.ModelForm):
    """
    Define the Profile Form
    """

    prefix = 'project'

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


class BaseArticleFormset(forms.BaseInlineFormSet):
    def clean(self):
        """
        Checks that no two positions have the same title.
        """
        if any(self.errors):
            return
        titles = []
        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):
                continue

            title = form.cleaned_data.get('title')
            title = str(title).lower()
            if str(title).lower() in titles:
                raise forms.ValidationError("Error: positions on a project must have distinct titles.")
            titles.append(title)

            key_skill = form.cleaned_data.get('key_skill')
            if key_skill and not title:
                raise forms.ValidationError("Error: enter a title for this position.")


#  Define the formset for Positions attached to a Project
position_inline_formset = forms.inlineformset_factory(
    models.Project,
    models.Position,
    formset=BaseArticleFormset,
    extra=1,
    fields=('title', 'description', 'key_skill'),
    widgets={
        'title': forms.TextInput(attrs={'placeholder': 'Position Title', 'class': 'circle--input--h3'}),
        'description': forms.Textarea(attrs={'placeholder': 'Position description...'},),
        'key_skill': forms.Select(attrs={'class': 'skill_selector'}),
    },
)


class DeleteProjectForm(forms.Form):
    class Meta:
        fields = ('title',)


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = models.UserApplication
        fields = (
            'position',
        )


class AcceptApplicationForm(forms.Form):
    applicant = forms.CharField()
    position = forms.CharField()

    class Meta:
        fields = (
            'applicant,'
            'position',
        )

