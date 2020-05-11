from django.contrib import admin
from . import models

admin.site.site_header = 'Teambuilder Admin Area'

# Register your models here.
admin.site.register(models.Profile)