from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.http import Http404, HttpResponseRedirect

from . import forms
from . import models


@login_required
def profile(request):
    return render(request, 'accounts/profile.html')


@login_required
def profile_test(request):
    return render(request, 'accounts/profile_test.html')


@login_required
def profile_edit(request):
    """
    Edit the User Profile.
    """
    user = request.user
    profile_form = forms.ProfileForm(prefix="profile")
    # skill_form = forms.UserSkill(prefix="skill")
    avatar_form = forms.AvatarForm

    # Get list of pre-defined skills
    try:
        skills = models.Skill.objects.all().order_by('name')
    except ObjectDoesNotExist:
        raise Http404

    predefined_skills = [(skill.id, skill.name) for skill in skills]
    skill_form = forms.UserSkill(choices=predefined_skills, prefix="skill")

    if request.method == 'POST' and 'update_profile' in request.POST:  # Profile form submitted
        try:
            user.profile = request.user.profile
        except models.Profile.DoesNotExist:
            user.profile = models.Profile(user=request.user)
        #
        # try:
        #     user.skill = models.UserSkill.objects.get(user=user.id)
        # except models.UserSkill.DoesNotExist:
        #     user_skill = models.UserSkill(user=user)

        profile_form = forms.ProfileForm(data=request.POST, instance=user.profile, prefix="profile")
        skill_form = forms.UserSkill(choices=predefined_skills, data=request.POST, prefix="skill")
        print(skill_form.data)

        if profile_form.is_valid() or skill_form.is_valid():
            profile_form.save()
            skill_form.save()
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

        avatar_form = forms.AvatarForm(data=request.POST, instance=user.profile, files=request.FILES)

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
            profile_form = forms.ProfileForm(
                initial={
                    'fullname': fullname,
                    'bio': bio
                }, prefix='profile')
            # skill_form = forms.UserSkill(prefix='skill')
        except models.Profile.DoesNotExist:
            profile_form = forms.ProfileForm

    return render(request, 'accounts/profile_edit.html', {
        'current_user': request.user,
        'profile_form': profile_form,
        'skill_form': skill_form,
        'avatar_form': avatar_form,
    })

