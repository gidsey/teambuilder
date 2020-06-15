from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect
from itertools import chain

from . import forms
from . import models


@login_required
def profile(request):
    user_skills = models.Skill.objects.all().filter(
        skill_user__user=request.user,
        skill_user__is_skill=True
    ).extra(select={'lower_name': 'lower(name)'}).order_by('lower_name')
    user_portfolios = models.Portfolio.objects.all().filter(
        user_id=request.user
    )
    return render(request, 'accounts/profile.html', {
        'user_skills': user_skills,
        'user_portfolios': user_portfolios,
    })


@login_required
def profile_edit(request):
    """
    Edit the User Profile.
    """
    # Get list of custom skills for the current user
    try:
        user_skills = models.Skill.objects.all().filter(
            Q(type__exact='c'), skill_user__user_id=request.user
        )
    except ObjectDoesNotExist:
        raise Http404

    #  Combine user's custom skills with pre-defined skills into a single choices list
    skills = list(chain(user_skills, models.Skill.objects.all().filter(type__exact='p')))
    choices = [(skill.id, skill.name) for skill in skills]
    choices.sort(key=lambda tup: tup[1].lower())  # Order the list by skill (case insensitive)

    user = request.user

    if request.method == 'POST' and 'update_profile' in request.POST:  # Profile form submitted
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
        avatar_form = forms.AvatarForm(prefix='AvatarForm')
        dynamic_formset = forms.portfolio_inline_formset(data=request.POST, instance=user, prefix='folio-items')

        if profile_form.is_valid() and custom_skills_formset.is_valid() and dynamic_formset.is_valid():
            user_profile = profile_form.save(commit=False)

            # form_true = the skills that need to set to true for the current user
            form_true = [int(skill) for skill in profile_form.cleaned_data['skills']]

            #  Create a list of custom skills added by the user
            custom_skill_list = []
            for custom_skill_form in custom_skills_formset:
                skill = custom_skill_form.cleaned_data.get('name')
                if skill:  # prevent 'None' being saved to list
                    custom_skill_list.append(skill)

            #  Add the custom skills to the Skills model (if they don't already exist)
            for custom_skill in custom_skill_list:
                obj, created = models.Skill.objects.get_or_create(
                    name=custom_skill,
                    type='c'
                )
                form_true.append(obj.id)  # Append the new custom skills to the form_true list

            # Create 2 sets (form_true and db_skills):
            form_true = set(form_true)

            # db_skills = all the skills associated with the current user (set either true or false)
            db_skills = set(
                [skill.skill_id for skill in models.UserSkill.objects.all().filter(user_id=request.user.id)])

            # Use the sets to define which skills should be set to True and which to False
            set_to_false = db_skills - form_true
            set_to_true = form_true - set_to_false

            #  Update the UserSkill model
            for skill in set_to_false:
                models.UserSkill.objects.filter(user_id=request.user.id, skill_id=skill).update(is_skill=False)
            for skill in set_to_true:
                try:
                    existing = models.UserSkill.objects.get(user_id=request.user.id, skill_id=skill)
                    if not existing.is_skill:
                        models.UserSkill.objects.filter(user_id=request.user.id, skill_id=skill).update(
                            is_skill=True
                        )
                except ObjectDoesNotExist:
                    models.UserSkill.objects.create(user_id=request.user.id, skill_id=skill, is_skill=True)

            user_profile.save()
            dynamic_formset.save()
            messages.success(
                request,
                "Profile saved successfully."
            )
            return HttpResponseRedirect(reverse('accounts:profile'))

    elif request.method == 'POST' and 'update_profile' not in request.POST:  # Avatar form submitted
        try:
            user.profile = request.user.profile
        except models.Profile.DoesNotExist:
            user.profile = models.Profile(user=request.user)

        avatar_form = forms.AvatarForm(
            data=request.POST,
            instance=user.profile,
            files=request.FILES,
        )
        profile_form = forms.ProfileForm(
            choices=choices,
            data=request.POST,
            instance=user.profile,
            prefix="profile",
        )
        custom_skills_formset = forms.CustomSkillsFormSet(request.POST, prefix='CSForm')
        dynamic_formset = forms.portfolio_inline_formset(data=request.POST, instance=user, prefix='folio-items')

        if avatar_form.is_valid():
            avatar_form.save()
            messages.success(
                request,
                "Avatar added successfully."
            )
            return HttpResponseRedirect(reverse('accounts:profile_edit'))
    else:
        try:
            fullname = user.profile.fullname
            bio = user.profile.bio
            saved_skills = models.UserSkill.objects.all().filter(user_id=request.user.id, is_skill=True)
            saved_skills_tuple = tuple([skill.skill_id for skill in saved_skills])

            custom_skills_formset = forms.CustomSkillsFormSet(prefix='CSForm')
            profile_form = forms.ProfileForm(
                prefix='profile',
                choices=choices,
                initial={
                    'fullname': fullname,
                    'bio': bio,
                    'skills': saved_skills_tuple,
                },
            )
            avatar_form = forms.AvatarForm()
            dynamic_formset = forms.portfolio_inline_formset(instance=user, prefix='folio-items')

        except models.Profile.DoesNotExist:
            profile_form = forms.ProfileForm(prefix='profile', choices=choices)
            custom_skills_formset = forms.CustomSkillsFormSet(prefix='CSForm')
            avatar_form = forms.AvatarForm()
            dynamic_formset = forms.portfolio_inline_formset(instance=user, prefix='folio-items')

    return render(request, 'accounts/profile_edit.html', {
        'current_user': request.user,
        'profile_form': profile_form,
        'avatar_form': avatar_form,
        'custom_skills_formset': custom_skills_formset,
        'dynamic_formset': dynamic_formset,
    })
