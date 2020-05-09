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
def profile_create(request):
    """
    Populate the Profile after the user has been created.
    """
    profile_form = forms.ProfileForm()
    user = request.user
    if request.method == 'POST':
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

    return render(request, 'accounts/profile_create.html', {
        'profile_form': profile_form
    })




