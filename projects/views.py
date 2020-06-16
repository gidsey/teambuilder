from django.shortcuts import render


def project_listing(request):
    return render(request, 'projects/project_listing.html')


def project_new(request):
    return render(request, 'projects/project_new.html')


def project_detail(request, pk=None):
    pk = 1
    return render(request, 'projects/project_detail.html')
