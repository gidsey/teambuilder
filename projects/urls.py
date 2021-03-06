from django.urls import path

from . import views

app_name = "projects"

urlpatterns = [
    path('needs/<needs_filter>/', views.project_listing, name='project_listing'),
    path('new/', views.project_new, name='project_new'),
    path('search/', views.project_search, name='project_search'),
    path('applications/<username>/', views.applications, name='applications'),
    path('<pk>/', views.project_detail, name='project_detail'),
    path('<pk>/edit/', views.project_edit, name='project_edit'),
    path('<pk>/delete/', views.project_delete, name='project_delete'),

]
