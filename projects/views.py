from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied

from . import forms
from . import models


def project_listing(request):
    projects = models.Project.objects.prefetch_related('positions')
    return render(request, 'projects/project_listing.html', {
        'projects': projects,
    })


@login_required
def project_new(request):
    if request.method == 'POST':
        user = request.user
        user.project = models.Project(owner=request.user)
        print('user.project {}'.format(user.project))
        project_form = forms.ProjectForm(data=request.POST, instance=user.project)
        positions_formset = forms.position_inline_formset(
            data=request.POST,
            instance=user.project,
            prefix='position-items'
        )

        if project_form.is_valid() and positions_formset.is_valid():

            project = project_form.save()
            positions_formset.save()

            messages.success(
                request,
                "Project created successfully."
            )
            return redirect('projects:project_detail', pk=project.pk)
    else:
        project_form = forms.ProjectForm()
        positions_formset = forms.position_inline_formset(prefix='position-items')

    return render(request, 'projects/project_new.html', {
        'project_form': project_form,
        'positions_formset': positions_formset,
    })


@login_required
def project_edit(request, pk):
    """
    Edit the Project.
    """
    try:
        project = models.Project.objects.get(id=pk)
    except ObjectDoesNotExist:
        raise Http404

    #  Only allow users to edit their own projects
    if request.user != project.owner:
        raise PermissionDenied

    if request.method == 'POST':
        project_form = forms.ProjectForm(data=request.POST, instance=project)
        positions_formset = forms.position_inline_formset(
            data=request.POST,
            instance=project,
            prefix='position-items'
        )

        if project_form.is_valid() and positions_formset.is_valid():
            project = project_form.save()
            positions_formset.save()
            messages.success(
                request,
                "Project updated successfully."
            )
            return redirect('projects:project_detail', pk=project.pk)
    else:
        project_form = forms.ProjectForm(instance=project)
        positions_formset = forms.position_inline_formset(instance=project, prefix='position-items')

    return render(request, 'projects/project_new.html', {
        'project_form': project_form,
        'positions_formset': positions_formset,
    })








def project_detail(request, pk):
    """
    Show the project detail page
    """

    try:
        project = models.Project.objects.get(id=pk)
    except ObjectDoesNotExist:
        raise Http404

    project_positions = models.Position.objects.all().filter(
        project_id=project.id
    )

    return render(request, 'projects/project_detail.html', {
        'project': project,
        'project_positions': project_positions,
    })
