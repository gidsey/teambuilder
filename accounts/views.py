from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect

from . import forms


def sign_up(request):
    form = forms.SignUpForm()
    if request.method == 'POST':
        form = forms.SignUpForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            login(request, user)
            messages.success(
                request,
                "Account setup successfully! You've been signed in too."
            )
            return HttpResponseRedirect(reverse('projects:project_listing'))

    return render(request, 'accounts/sign_up.html', {
        'form': form,
    })


def sign_in(request):
    pass
