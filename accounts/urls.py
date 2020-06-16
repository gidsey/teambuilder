from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('profile/<username>/', views.user_profile, name='user_profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
]

