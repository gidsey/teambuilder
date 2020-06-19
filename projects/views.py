from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

from . import forms
from . import models


# def menu_list(request):
#     """List all menus whose expiry date is later than today."""
#     menus = models.Menu.objects.all().prefetch_related('items').filter(
#         expiration_date__gte=timezone.now()).order_by('-expiration_date')
#     return render(request, 'menu/menu_list.html', {'menus': menus})
#

def project_listing(request):
    projects = models.Project.objects.prefetch_related('positions')
    print(projects)
    for project in projects:
        print(project)
        print(project.positions)
    return render(request, 'projects/project_listing.html', {
        'projects': projects,
    })
#  project_positions = models.Position.objects.all().filter(project__owner=project.owner_id)

@login_required
def project_new(request):
    if request.method == 'POST':
        user = request.user
        user.project = models.Project(owner=request.user)
        project_form = forms.ProjectForm(data=request.POST, instance=user.project)
        positions_formset = forms.position_inline_formset(data=request.POST, instance=user.project, prefix='position-items')

        if project_form.is_valid() and positions_formset.is_valid():

            project = project_form.save()
            positions_formset.save()

            messages.success(
                request,
                "Project created successfully."
            )
            return redirect('projects:project_detail', pk=project.pk)
    else:
        user = request.user
        project_form = forms.ProjectForm()
        positions_formset = forms.position_inline_formset(prefix='position-items')

    return render(request, 'projects/project_new.html', {
        'project_form': project_form,
        'positions_formset': positions_formset,
    })


@login_required
def project_detail(request, pk):
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
