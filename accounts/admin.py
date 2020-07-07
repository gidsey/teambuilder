from django.contrib import admin
from .models import Skill, Profile

admin.site.site_header = 'Teambuilder Admin Area'


class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'type']
    ordering = ['-type']


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'fullname', 'bio', 'avatar']
    ordering = ['-fullname']


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Skill, SkillAdmin)
