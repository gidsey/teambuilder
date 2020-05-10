from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect

from . import forms
from . import models


def profile(request):
    return render(request, 'accounts/profile.html')


@login_required
def profile_test(request):
    return render(request, 'accounts/profile_test.html')


@login_required
def profile_create(request):
    """
    Populate the Profile after the user has been created.
    """
    profile_form = forms.ProfileForm()
    avatar_form = forms.AvatarForm()
    user = request.user

    #  Profile Changes
    if request.method == 'POST':
        if 'update_profile' in request.POST:
            try:
                user.profile = request.user.profile  # Set Profile instance for the current user
            except models.Profile.DoesNotExist:
                user.profile = models.Profile(user=request.user)  # Set the Profile instance for a new user

            profile_form = forms.ProfileForm(data=request.POST, instance=user.profile)

            if profile_form.is_valid():
                profile_form.save()
                messages.success(
                    request,
                    "Profile saved successfully."
                )
                return HttpResponseRedirect(reverse('accounts:profile'))

        else:
            try:
                user.profile = request.user.profile  # Set Profile instance for the current user
            except models.Profile.DoesNotExist:
                user.profile = models.Profile(user=request.user)  # Set the Profile instance for a new user
            avatar_form = forms.AvatarForm(instance=user.profile, data=request.POST, files=request.FILES)

            if avatar_form.is_valid():
                avatar_form.save()
                messages.success(
                    request,
                    "Avatar image updated successfully."
                )
                return HttpResponseRedirect(reverse('accounts:profile_create'))

    return render(request, 'accounts/profile_create.html', {
        'current_user': request.user,
        'profile_form': profile_form,
        'avatar_form': avatar_form,
    })




