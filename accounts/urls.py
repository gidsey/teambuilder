from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    # path('profile/', views.profile, name='profile'),
    path('profile/<username>/edit/', views.profile_edit, name='user_profile_edit'),
    path('profile/<username>/', views.user_profile, name='user_profile'),

]

