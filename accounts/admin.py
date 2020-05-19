from django.contrib import admin
from . import models

admin.site.site_header = 'Teambuilder Admin Area'

admin.site.register(models.Profile)
admin.site.register(models.Skill)
