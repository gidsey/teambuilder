from django.urls import path

from . import views

app_name = "projects"  # required when using namespace in URLS

urlpatterns = [
    path('', views.project_listing, name='project_listing'),
    path('new/', views.project_new, name='project_new'),
    path('<pk>/edit', views.project_edit, name='project_edit'),
    path('<pk>/', views.project_detail, name='project_detail')
]
