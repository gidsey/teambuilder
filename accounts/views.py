from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.http import Http404, HttpResponseRedirect

from .utils import machine_name

from . import forms
from . import models


@login_required
def profile(request):
    user_skills = models.Skill.objects.all().filter(
        skill_user__user=request.user,
        skill_user__is_skill=True
    ).extra(select={'lower_name': 'lower(name)'}).order_by('lower_name')
    return render(request, 'accounts/profile.html', {
        'user_skills': user_skills,
    })


@login_required
def profile_edit(request):
    """
    Edit the User Profile.
    """
    # Get list of pre-defined skills
    try:
        skills = models.Skill.objects.all().order_by('name')
    except ObjectDoesNotExist:
        raise Http404

    # predefined_skills = [(machine_name(str(skill)), str(skill)) for skill in skills]
    predefined_skills = [(skill.id, skill.name) for skill in skills]
    predefined_skills.sort(key=lambda tup: tup[1].lower())
    user = request.user
    # profile_form = forms.ProfileForm(choices=predefined_skills, prefix="profile")
    avatar_form = forms.AvatarForm

    if request.method == 'POST' and 'update_profile' in request.POST:  # Profile form submitted
        try:
            user.profile = request.user.profile
        except models.Profile.DoesNotExist:
            user.profile = models.Profile(user=request.user)

        profile_form = forms.ProfileForm(
            choices=predefined_skills,
            data=request.POST,
            instance=user.profile,
            prefix="profile",
        )

        custom_skills_formset = forms.CustomSkillsFormSet(request.POST, prefix='CSForm')

        if profile_form.is_valid() and custom_skills_formset.is_valid():
            user_profile = profile_form.save(commit=False)
            custom_skill_list = []

            db_true = set([skill.skill_id for skill in models.UserSkill.objects.all().filter(user_id=request.user.id)])
            form_true = [int(skill) for skill in profile_form.cleaned_data['skills']]

            for custom_skill_form in custom_skills_formset:
                skill = custom_skill_form.cleaned_data.get('name')
                if skill:  # prevent 'None' being saved to list
                    custom_skill_list.append(skill)

            print('custom_skill_list: {}'.format(custom_skill_list))

            for custom_skill in custom_skill_list:
                obj, created = models.Skill.objects.get_or_create(
                    name=custom_skill,
                    type='c'
                )
                print('obj {}'.format(obj))
                print('created {}'.format(created))
                print('obj.id {}'.format(obj.id))
                form_true.append(obj.id)

            form_true = set(form_true)
            set_to_false = db_true - form_true
            set_to_true = form_true - set_to_false

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
            messages.success(
                request,
                "Profile saved successfully."
            )
            return HttpResponseRedirect(reverse('accounts:profile'))

    # elif request.method == 'POST' and 'update_profile' not in request.POST:  # Avatar form submitted
    #     try:
    #         user.profile = request.user.profile
    #     except models.Profile.DoesNotExist:
    #         user.profile = models.Profile(user=request.user)
    #
    #     avatar_form = forms.AvatarForm(data=request.POST, instance=user.profile, files=request.FILES)
    #
    #     if avatar_form.is_valid():
    #         avatar_form.save()
    #         messages.success(
    #             request,
    #             "Avatar added successfully."
    #         )
    #         return HttpResponseRedirect(reverse('accounts:profile_edit'))
    else:
        try:
            fullname = user.profile.fullname
            bio = user.profile.bio
            saved_skills = models.UserSkill.objects.all().filter(user_id=request.user.id, is_skill=True)
            saved_skills_tuple = tuple([skill.skill_id for skill in saved_skills])
            custom_skills_formset = forms.CustomSkillsFormSet(prefix='CSForm')
            profile_form = forms.ProfileForm(
                prefix='profile',
                choices=predefined_skills,
                initial={
                    'fullname': fullname,
                    'bio': bio,
                    'skills': saved_skills_tuple,
                },

            )

        except models.Profile.DoesNotExist:
            profile_form = forms.ProfileForm(prefix='profile', choices=predefined_skills)
            custom_skills_formset = forms.CustomSkillsFormSet(prefix='CSForm')

    return render(request, 'accounts/profile_edit.html', {
        'current_user': request.user,
        'profile_form': profile_form,
        'avatar_form': avatar_form,
        'custom_skills_formset': custom_skills_formset,
    })
