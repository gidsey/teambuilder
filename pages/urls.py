from django.urls import path
from .views import AboutPageView, index

app_name = "pages"

urlpatterns = [
    path('', index, name='index'),
    path('about/', AboutPageView.as_view(), name='about')
]