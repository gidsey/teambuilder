from django.shortcuts import render


def project_listing(request):
    return render(request, 'projects/project_listing.html')