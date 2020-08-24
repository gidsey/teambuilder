from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path('profile/edit/', views.profile_edit_redirect, name='profile_edit_redirect'),
    path('profile/<username>/edit/', views.user_profile_edit, name='user_profile_edit'),
    path('profile/<username>/', views.user_profile, name='user_profile'),

]

