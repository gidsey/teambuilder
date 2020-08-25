from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView


def index(request):
    url = reverse('projects:project_listing', kwargs={'needs_filter': 'all'})
    return HttpResponseRedirect(url)


class AboutPageView(TemplateView):
    template_name = 'about.html'




