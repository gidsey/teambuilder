from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.urls import reverse
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect
from itertools import chain

from .utils import get_skill_sets, get_saved_skills

from . import forms
from . import models
from projects.models import Project


def user_profile(request, username):
    """
    Show the user profile page
    """
    try:
        profile_user = models.User.objects.get(username=username)
    except ObjectDoesNotExist:
        raise Http404

    profile_user_skills = models.Skill.objects.all().filter(
        skill_user__user=profile_user,
        skill_user__is_skill=True
    ).extra(select={'lower_name': 'lower(name)'}).order_by('lower_name')
    profile_user_portfolios = models.Portfolio.objects.all().filter(
        user_id=profile_user
    )
    profile_projects = Project.objects.prefetch_related('positions').filter(owner=profile_user)
    return render(request, 'accounts/profile.html', {
        'profile_user': profile_user,
        'profile_user_skills': profile_user_skills,
        'profile_user_portfolios': profile_user_portfolios,
        'profile_projects': profile_projects,
    })


@login_required
def profile_edit_redirect(request):
    """
    Redirect the user on first login to
    their profile edit page.
    """
    return HttpResponseRedirect(reverse('accounts:user_profile_edit', args={request.user}))


@login_required
def user_profile_edit(request, username):
    """
    Create and/or edit the User Profile.
    """
    # Get list of custom skills for the current user
    try:
        user_skills = models.Skill.objects.filter(Q(type__exact='c'), skill_user__user_id=request.user)
    except ObjectDoesNotExist:
        raise Http404

    #  Only allow users to edit their own profile
    user = request.user
    if username != user.username:
        raise PermissionDenied

    #  Combine user's custom skills with pre-defined skills into a single choices list
    skills = list(chain(user_skills, models.Skill.objects.all().filter(type__exact='p')))
    choices = [(skill.id, skill.name) for skill in skills]
    choices.sort(key=lambda tup: tup[1].lower())  # Order the list by skill (case insensitive)

    if request.method == 'POST':
        try:
            user.profile = request.user.profile
        except models.Profile.DoesNotExist:
            user.profile = models.Profile(user=request.user)

        profile_form = forms.ProfileForm(
            choices=choices,
            data=request.POST,
            instance=user.profile,
            prefix="profile",
        )

        custom_skills_formset = forms.CustomSkillsFormSet(request.POST, prefix='CSForm')
        dynamic_formset = forms.portfolio_inline_formset(data=request.POST, instance=user, prefix='folio-items')
        avatar_form = forms.AvatarForm(data=request.POST, instance=user.profile, files=request.FILES)

        if (profile_form.is_valid()
                and custom_skills_formset.is_valid()
                and dynamic_formset.is_valid()
                and avatar_form.is_valid()):

            if avatar_form.cleaned_data['x']:
                avatar_form.save()  # only save the avatar if a new image has been uploaded

            user_profile_form = profile_form.save(commit=False)

            # Check which skills should be set to true and which to false
            skill_sets = get_skill_sets(request, profile_form, custom_skills_formset)
            set_to_false = skill_sets[0]
            set_to_true = skill_sets[1]

            #  Update the UserSkill table
            for skill in set_to_false:
                models.UserSkill.objects.filter(user_id=request.user.id, skill_id=skill).update(is_skill=False)
            for skill in set_to_true:
                try:
                    existing = models.UserSkill.objects.get(user_id=request.user.id, skill_id=skill)
                    if not existing.is_skill:
                        models.UserSkill.objects.filter(user_id=request.user.id, skill_id=skill).update(is_skill=True)
                except ObjectDoesNotExist:
                    models.UserSkill.objects.create(user_id=request.user.id, skill_id=skill, is_skill=True)

            user_profile_form.save()
            dynamic_formset.save()

            messages.success(
                request,
                "Profile saved successfully."
            )
            return HttpResponseRedirect(reverse('accounts:user_profile', args={username}))
    else:
        try:   # edit existing user
            fullname = user.profile.fullname
            bio = user.profile.bio
            saved_skills = get_saved_skills(user)

            profile_form = forms.ProfileForm(
                prefix='profile',
                choices=choices,
                initial={
                    'fullname': fullname,
                    'bio': bio,
                    'skills': saved_skills,
                },
            )

        except ObjectDoesNotExist:  # new user
            profile_form = forms.ProfileForm(prefix='profile', choices=choices)

    custom_skills_formset = forms.CustomSkillsFormSet(prefix='CSForm')
    avatar_form = forms.AvatarForm()
    dynamic_formset = forms.portfolio_inline_formset(instance=user, prefix='folio-items')
    profile_projects = Project.objects.prefetch_related('positions').filter(owner=user)

    return render(request, 'accounts/profile_edit.html', {
        'current_user': request.user,
        'profile_form': profile_form,
        'avatar_form': avatar_form,
        'custom_skills_formset': custom_skills_formset,
        'dynamic_formset': dynamic_formset,
        'profile_projects': profile_projects,
    })
