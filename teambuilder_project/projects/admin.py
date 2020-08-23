from django.contrib import admin
from datetime import date

from .models import Project, Position, UserApplication


class PositionInline(admin.StackedInline):
    model = Position


class YearListFilter(admin.SimpleListFilter):
    title = 'year created'
    parameter_name = 'year'

    def lookups(self, request, model_admin):
        return (
            ('2019', '2019'),
            ('2020', '2020'),
            ('2021', '2021'),
        )

    def queryset(self, request, queryset):
        if self.value():
            year = int(self.value())
            return queryset.filter(created_at__gte=date(year, 1, 1),
                                   created_at__lte=date(year, 12, 31))


class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'timeline',
        'requirements',
        'owner',
        'created_at',
    ]
    inlines = [PositionInline]
    ordering = ['-created_at']
    search_fields = ['title', 'requirements']
    list_filter = ['created_at', YearListFilter]


class PositionAdmin(admin.ModelAdmin):
    list_display = [
        'project',
        'title',
        'filled',
    ]
    ordering = ['title']
    list_filter = ['filled', 'title', ]


class UserApplicationAdmin(admin.ModelAdmin):
    list_display = [
        'position',
        'user',
        'status',
        'created_at',
    ]
    ordering = ['-created_at']
    list_filter = ['user', 'status', 'created_at']


admin.site.register(Project, ProjectAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(UserApplication, UserApplicationAdmin)
