from django.urls import path

from . import views

app_name = "accounts"  # required when using namespace in URLS

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('profile/create/', views.profile_create, name='profile_create'),
    path('profile/test/', views.profile_test, name='profile_test'),


    # path('profile/edit/', views.profile_edit, name='profile_edit'),



    # path('sign_out/', views.sign_out, name='sign_out'),
    # path('create_profile/', views.create_profile, name='create_profile'),
    # path('profile/edit/', views.edit_profile, name='edit_profile'),
    # path('profile/', views.profile, name='profile'),
    # path('profile/change_password', views.change_password, name='change_password'),
]

