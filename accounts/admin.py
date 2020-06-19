from django.contrib import admin
from .models import Skill, Profile

admin.site.site_header = 'Teambuilder Admin Area'


class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'type']
    ordering = ['-type']


admin.site.register(Profile)
admin.site.register(Skill, SkillAdmin)
