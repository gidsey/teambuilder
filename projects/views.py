from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.db.models import Q

from .utils import get_project_needs, get_search_term
from . import forms
from . import models


def project_listing(request):
    """
    Return a list of all Projects
    and Project Needs.
    """
    projects = models.Project.objects.order_by('-created_date').prefetch_related('positions')
    project_needs = get_project_needs(projects)
    num_projects = len(projects)
    return render(request, 'projects/project_listing.html', {
        'projects': projects,
        'project_needs': project_needs,
        'num_projects': num_projects,
    })


def project_listing_filtered(request, needs_filter):
    """
    Return the filtered list of Projects
    based on Project Needs.
    """
    all_projects = models.Project.objects.prefetch_related('positions')
    project_needs = get_project_needs(all_projects)
    search_term = get_search_term(needs_filter, project_needs)

    projects = all_projects.order_by('-created_date').filter(
        positions__title=search_term
    )
    num_projects = len(projects)
    return render(request, 'projects/project_listing.html', {
        'projects': projects,
        'project_needs': project_needs,
        'num_projects': num_projects,
    })


@login_required
def project_new(request):
    """
    Create a new Project
    and associated Positions.
    """
    if request.method == 'POST':
        user = request.user
        user.project = models.Project(owner=request.user)
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

    return render(request, 'projects/project_new_edit.html', {
        'mode': 'create',
        'project_form': project_form,
        'positions_formset': positions_formset,
    })


@login_required
def project_edit(request, pk):
    """
    Edit a Project
    and associated Positions.
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

    return render(request, 'projects/project_new_edit.html', {
        'pk': pk,
        'mode': 'edit',
        'project_form': project_form,
        'positions_formset': positions_formset,
    })


@login_required
def project_detail(request, pk):
    """
    Show the project detail page.
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


@login_required
def project_delete(request, pk):
    """
    Delete the Project.
    """
    try:
        project = models.Project.objects.get(id=pk)
    except ObjectDoesNotExist:
        raise Http404

    #  Only allow users to edit their own projects
    if request.user != project.owner:
        raise PermissionDenied

    if request.method == 'POST':
        delete_form = forms.DeleteProjectForm(data=request.POST)
        if delete_form.is_valid():
            project.delete()
            messages.success(
                request,
                "Project deleted successfully."
            )
            return redirect('projects:project_listing')
    else:
        delete_form = forms.DeleteProjectForm()

    return render(request, 'projects/project_delete.html', {
        'project': project,
        'delete_form': delete_form,
    })


def project_search(request):
    """
    Search Project based on words in
    their title or description.
    """
    term = request.GET.get('q')
    projects = models.Project.objects.prefetch_related('positions')
    project_needs = get_project_needs(projects)
    search_results = projects.filter(
        Q(title__icontains=term) |
        Q(description__icontains=term)
    )
    num_results = len(search_results)

    return render(request, 'projects/project_search.html', {
        'projects': projects,
        'project_needs': project_needs,
        'term': term,
        'search_results': search_results,
        'num_results': num_results,
    })


@login_required
def applications(request, username):
    try:
        profile_user = models.User.objects.get(username=username)
    except ObjectDoesNotExist:
        raise Http404

    #  Only allow users to view their own applications page
    if request.user != profile_user:
        raise PermissionDenied

    user_projects = models.Project.objects.prefetch_related('positions').filter(owner=profile_user)

    project_needs = []
    for project in user_projects:
        for position in project.positions.all():
            if position.title not in project_needs:
                project_needs.append(position.title)
    project_needs = sorted(project_needs, key=str.casefold)
    print(project_needs)

    return render(request, 'projects/applications.html', {
        'profile_user': profile_user,
        'user_projects': user_projects,
        'project_needs': project_needs,
    })
