from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect

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
    profile_form = forms.ProfileForm
    skill_form = forms.SkillForm
    avatar_form = forms.AvatarForm

    if request.method == 'POST' and 'update_profile' in request.POST:  # Profile form submitted
        try:
            user.profile = request.user.profile
        except models.Profile.DoesNotExist:
            user.profile = models.Profile(user=request.user)

        profile_form = forms.ProfileForm(data=request.POST, instance=user.profile)

        if profile_form.is_valid():
            profile_form.save()
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
                })
        except models.Profile.DoesNotExist:
            profile_form = forms.ProfileForm

    return render(request, 'accounts/profile_edit.html', {
        'current_user': request.user,
        'profile_form': profile_form,
        'skill_form': skill_form,
        'avatar_form': avatar_form,
    })

