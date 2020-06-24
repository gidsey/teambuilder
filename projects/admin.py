from django.contrib import admin

from .models import Project, Position


class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        'owner',
        'title',
        'description',
        'timeline',
        'requirements',
        'created_at',
    ]
    ordering = ['-created_at']


class PositionAdmin(admin.ModelAdmin):
    list_display = [
        'project',
        'title',
        'description',
    ]
    ordering = ['title']


admin.site.register(Project, ProjectAdmin)
admin.site.register(Position, PositionAdmin)
