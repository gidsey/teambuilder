
from django.urls import reverse
from django.http import HttpResponseRedirect


def index(request):
    return HttpResponseRedirect(reverse("projects:project_listing"))

