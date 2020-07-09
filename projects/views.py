from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q

from .utils import (get_slugified_list, get_search_term, get_project_needs,
                    send_application_received_mail, send_application_result_mail,
                    get_skill_choices, get_skill_sets)
from . import forms
from . import models
from accounts.models import Skill, UserSkill


def project_listing(request, needs_filter):
    """
    Return the filtered list of Projects
    based on Project Needs.
    """
    all_projects = models.Project.objects.prefetch_related('positions', 'project_skill__skill').order_by('-created_at')
    num_projects = filtered_num_projects = len(all_projects)
    project_needs = get_project_needs(all_projects)

    if needs_filter == 'all':
        projects = all_projects
        search_term = 'all'
    elif needs_filter == 'suggested':
        if request.user.is_authenticated:
            for project in all_projects:
                print(project.project_skill.all())

            user_skills = UserSkill.objects.all().select_related('skill').filter(user_id=request.user)


            print(user_skills)
            user_skillset = [skill.skill for skill in user_skills]
            print(user_skillset)
            projects = set(all_projects.order_by('-created_at').filter(
                Q(project_skill__skill__in=user_skills) &
                ~Q(owner__exact=request.user)))
            search_term = 'suggested'
            filtered_num_projects = len(projects)
            totals = (num_projects, filtered_num_projects)
        else:
            raise PermissionDenied

    else:
        search_term = get_search_term(needs_filter, project_needs)
        projects = all_projects.order_by('-created_at').filter(positions__title=search_term)
        filtered_num_projects = len(projects)
    totals = (num_projects, filtered_num_projects)

    return render(request, 'projects/project_listing.html', {
        'projects': projects,
        'project_needs': project_needs,
        'search_term': search_term,
        'totals': totals,
    })


@login_required
def project_new(request):
    """
    Create a new Project
    and associated Positions.
    """
    available_skills = Skill.objects.all()
    choices = get_skill_choices(available_skills)

    if request.method == 'POST':
        user = request.user
        user.project = models.Project(owner=request.user)
        project_form = forms.ProjectForm(data=request.POST, instance=user.project)
        project_skills_form = forms.ProjectSkillsForm(choices=choices, data=request.POST)
        positions_formset = forms.position_inline_formset(
            data=request.POST,
            instance=user.project,
            prefix='position-items'
        )

        if project_form.is_valid() and positions_formset.is_valid() and project_skills_form.is_valid():
            project = project_form.save()
            positions_formset.save()
            skills = project_skills_form.cleaned_data['project_skills']
            for skill in skills:
                skill_instance = available_skills.get(id=skill)
                models.ProjectSkill.objects.create(project=project, skill=skill_instance, required_skill=True)
            messages.success(request, "Project created successfully.")
            return redirect('projects:project_detail', pk=project.pk)
    else:
        project_form = forms.ProjectForm()
        positions_formset = forms.position_inline_formset(prefix='position-items')
        project_skills_form = forms.ProjectSkillsForm(choices=choices)

    return render(request, 'projects/project_new_edit.html', {
        'mode': 'create',
        'project_form': project_form,
        'positions_formset': positions_formset,
        'project_skills_form': project_skills_form,
    })


@login_required
def project_edit(request, pk):
    """
    Edit a Project
    and associated Positions.
    """
    try:
        project = models.Project.objects.select_related(
            'owner__profile'
        ).prefetch_related(
            'positions__application_position__user',
            'project_skill__skill'
        ).get(
            id=pk
        )
    except ObjectDoesNotExist:
        raise Http404

    #  Only allow users to edit their own projects
    if request.user != project.owner:
        raise PermissionDenied

    # Get a list of all available skills to populate the skills checkboxes
    available_skills = Skill.objects.all()
    choices = get_skill_choices(available_skills)

    # Get the initial values for the skills checkboxes
    checked_skills = project.project_skill.filter(required_skill=True)
    initial = tuple([skill.skill_id for skill in checked_skills])

    if request.method == 'POST':
        project_form = forms.ProjectForm(data=request.POST, instance=project)
        project_skills_form = forms.ProjectSkillsForm(choices=choices, initial={'project_skills': initial}, data=request.POST)
        positions_formset = forms.position_inline_formset(
            data=request.POST,
            instance=project,
            prefix='position-items'
        )

        if project_form.is_valid() and positions_formset.is_valid() and project_skills_form.is_valid():
            project = project_form.save()
            positions_formset.save()

            # Check which skills should be set to true and which to false
            skill_sets = get_skill_sets(project_skills_form, pk)
            set_to_false = skill_sets[0]
            set_to_true = skill_sets[1]

            #  Update the ProjectSkill model
            for skill in set_to_false:
                models.ProjectSkill.objects.filter(project_id=pk, skill_id=skill).update(required_skill=False)
            for skill in set_to_true:
                try:
                    existing = models.ProjectSkill.objects.get(project_id=pk, skill_id=skill)
                    if not existing.required_skill:
                        models.ProjectSkill.objects.filter(project_id=pk, skill_id=skill).update(
                            required_skill=True
                        )
                except ObjectDoesNotExist:
                    models.ProjectSkill.objects.create(project_id=pk, skill_id=skill, required_skill=True)

            messages.success(request, "Project updated successfully.")
            return redirect('projects:project_detail', pk=project.pk)
    else:
        project_form = forms.ProjectForm(instance=project)
        positions_formset = forms.position_inline_formset(instance=project, prefix='position-items')
        project_skills_form = forms.ProjectSkillsForm(choices=choices, initial={'project_skills': initial})

    return render(request, 'projects/project_new_edit.html', {
        'pk': pk,
        'mode': 'edit',
        'project_form': project_form,
        'positions_formset': positions_formset,
        'project_skills_form': project_skills_form,
    })


@login_required
def project_detail(request, pk):
    """
    Show the project detail page.
    """
    try:
        project = models.Project.objects.select_related(
            'owner__profile',
        ).prefetch_related(
            'positions__application_position__user',
            'project_skill__skill',
        ).get(
            id=pk
        )
    except ObjectDoesNotExist:
        raise Http404

    required_skills = project.project_skill.filter(required_skill=True)

    if request.method == 'POST':
        application_form = forms.ApplicationForm(data=request.POST)
        if application_form.is_valid():
            application = application_form.save(commit=False)
            position = application_form.cleaned_data['position']
            application.user = request.user
            application.save()
            messages.success(request, "Application received.")
            send_application_received_mail(
                email_to=application.user.email,
                name=application.user.profile.fullname,
                position=position,
                project=project
            )
            return render(request, 'projects/application_confirm.html', {
                'position': position,
            })

    else:
        application_form = forms.ApplicationForm()

    return render(request, 'projects/project_detail.html', {
        'project': project,
        'required_skills': required_skills,
        'application_form': application_form,
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
            return HttpResponseRedirect(reverse('projects:project_listing', args={'all'}))
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
    projects = models.Project.objects.prefetch_related('positions').order_by('-created_at')
    project_needs = get_project_needs(projects)
    search_term = 'all'
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
        'search_term': search_term,
    })


@login_required
def applications(request, username):
    #  Get the user based on the supplied username
    try:
        profile_user = models.User.objects.get(username=username)
    except ObjectDoesNotExist:
        raise Http404

    #  Only allow users to view their own applications page
    if request.user != profile_user:
        raise PermissionDenied

    #  Retrieve the URL query strings (set to 'all' or '123' if not supplied)
    status = request.GET.get('s', '123')
    proj = request.GET.get('p', 'all')
    need = request.GET.get('n', 'all')
    m_status = [status, proj, need]

    #  Get all the projects owned by the user
    all_user_projects = models.Project.objects.all().prefetch_related('positions').filter(owner=profile_user)

    # Make a (slugified, Display Name) list of the user's projects
    project_list = get_slugified_list(all_user_projects)

    # Make a (slugified, Display Name) list of project needs associated with the user's projects
    project_needs = get_project_needs(all_user_projects)

    # Get the search term based on the slugified term supplied in the URL query string
    proj_term = get_search_term(proj, project_list)
    need_term = get_search_term(need, project_needs)

    # Set defaults and identify the search type (1 to 4)
    # filter the all_user_projects queryset accordingly
    search_type = 1
    # user_projects = all_user_projects

    #  All Projects and all Needs
    if proj == 'all' and need == 'all':
        search_type = 1
        user_projects = all_user_projects

    #  All Needs, filtered Projects
    elif need == 'all' and proj != 'all':
        search_type = 2
        user_projects = all_user_projects.filter(title=proj_term)

    #  All Projects, filtered Needs
    elif need != 'all' and proj == 'all':
        search_type = 3
        user_projects = all_user_projects.filter(positions__title__exact=need_term)

    # Filters Projects and filtered Needs
    elif proj != 'all' and need != 'all':
        search_type = 4
        user_projects = all_user_projects.filter(
            Q(title=proj_term) &
            Q(positions__title=need_term))

    #  Get all the applications on projects owned by the user
    user_applications = models.UserApplication.objects.filter(position__project__owner=request.user)

    total_num_app = len(user_applications)

    #  Filter the applications based on status and user_projects
    all_applications = user_applications.filter(
        Q(status__in=status) &
        Q(position__project__in=user_projects)
    ).prefetch_related(
        'position', 'position__project', 'user__profile'
    ).order_by('status', '-created_at')

    if search_type == 3 or search_type == 4:
        all_applications = all_applications.filter(position__title__exact=need_term)

    # Count the number of filtered results
    filtered_num_app = len(all_applications)
    totals = [total_num_app, filtered_num_app]

    #  Handle the Accept / Reject buttons
    if request.method == 'POST':
        accept_form = forms.AcceptApplicationForm(data=request.POST)
        if accept_form.is_valid():
            applicant = accept_form.cleaned_data['applicant']
            position_sought = accept_form.cleaned_data['position']

            if request.POST.get("accept"):
                status = 2
                msg = "Application accepted"
                email_msg = 'accept'
            elif request.POST.get("reject"):
                status = 3
                msg = "Application rejected"
                email_msg = 'reject'
            try:
                app = models.UserApplication.objects.filter(
                    user_id=applicant,
                    position_id=position_sought,
                )
            except ObjectDoesNotExist:
                raise Http404

            #  Update the application status
            app.update(status=status)

            #  If application successful, mark the position as filled and reject any other applicants.
            if status == 2:
                unsuccessful_applicants = user_applications.filter(position_id=position_sought, status=1)
                if unsuccessful_applicants:
                    for unsuccessful_applicant in unsuccessful_applicants:
                        send_application_result_mail(
                            status='reject',
                            applicant=unsuccessful_applicant.user.id,
                            position_sought=position_sought,
                            )

                    unsuccessful_applicants.update(status=3)

                filled = models.Position.objects.filter(id=position_sought)
                filled.update(filled=True)

            #  Alert the user via in-app message and email
            messages.success(request, msg)
            send_application_result_mail(
                status=email_msg,
                applicant=applicant,
                position_sought=position_sought,
            )
            return render(request, 'projects/application_confirm.html', {
            })

    else:
        accept_form = forms.AcceptApplicationForm()

    return render(request, 'projects/applications.html', {
        'profile_user': profile_user,
        'user_projects': user_projects,
        'project_needs': project_needs,
        'project_list': project_list,
        'all_applications': all_applications,
        'accept_form': accept_form,
        'm_status': m_status,
        'totals': totals,
    })
