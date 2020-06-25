
from django.urls import reverse
from django.http import HttpResponseRedirect


def index(request):
    url = reverse('projects:project_listing', kwargs={'needs_filter': 'all'})
    return HttpResponseRedirect(url)

