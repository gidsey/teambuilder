from django.contrib import admin
from .models import Skill, Profile

admin.site.site_header = 'Teambuilder Admin Area'


class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'type']
    list_editable = ['type']
    ordering = ['-type']


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['fullname', 'user']
    ordering = ['fullname']
    search_fields = ['fullname']


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Skill, SkillAdmin)
