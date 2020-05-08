from django.shortcuts import render


def profile(request):
    return render(request, 'accounts/profile.html')


def profile_create(request):
    return render(request, 'accounts/profile_create.html')



