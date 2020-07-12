from django.contrib import admin

from .models import Project, Position, UserApplication


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
        'filled',
    ]
    ordering = ['title']


class UserApplicationAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'position',
        'status',
        'created_at',
    ]
    ordering = ['-created_at']


admin.site.register(Project, ProjectAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(UserApplication, UserApplicationAdmin)
