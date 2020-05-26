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
    return render(request, 'accounts/profile.html')


@login_required
def profile_test(request):
    return render(request, 'accounts/profile_test.html')


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

    predefined_skills = [(machine_name(str(skill)), str(skill)) for skill in skills]
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
            prefix="profile"
        )

        if profile_form.is_valid():
            print('profile_form.data {}'.format(profile_form.data))
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
                prefix='profile',
                choices=predefined_skills,
                initial={
                    'fullname': fullname,
                    'bio': bio
                })

        except models.Profile.DoesNotExist:
            profile_form = forms.ProfileForm(prefix='profile', choices=predefined_skills)

    return render(request, 'accounts/profile_edit.html', {
        'current_user': request.user,
        'profile_form': profile_form,
        'avatar_form': avatar_form,
    })

