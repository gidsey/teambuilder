from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

from . import forms
from . import models


def project_listing(request):
    return render(request, 'projects/project_listing.html')


@login_required
def project_new(request):
    if request.method == 'POST':
        user = request.user
        user.project = models.Project(owner=request.user)
        project_form = forms.ProjectForm(data=request.POST, instance=user.project)

        if project_form.is_valid():
            print(project_form.cleaned_data['title'])
            project = project_form.save()
            messages.success(
                request,
                "Project created successfully."
            )
            return redirect('projects:project_detail', pk=project.pk)
    else:
        project_form = forms.ProjectForm()

    return render(request, 'projects/project_new.html', {
        'project_form': project_form
    })


@login_required
def project_detail(request, pk):
    try:
        project = models.Project.objects.get(id=pk)
    except ObjectDoesNotExist:
        raise Http404

    return render(request, 'projects/project_detail.html', {
        'project': project
    })
