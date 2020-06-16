from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse

from . import forms
from . import models


def project_listing(request):
    return render(request, 'projects/project_listing.html')


@login_required
def project_new(request):
    if request.method == 'POST':
        project_form = forms.ProjectForm(data=request.POST, instance=request.user)

        if project_form.is_valid():
            project_form.save()
            messages.success(
                request,
                "Profile saved successfully."
            )
            return HttpResponseRedirect(reverse('projects:project_detail'))
    else:
        project_form = forms.ProjectForm()

    return render(request, 'projects/project_new.html', {
        'project_form': project_form
    })


@login_required
def project_detail(request, pk=None):
    pk = 1
    return render(request, 'projects/project_detail.html')
