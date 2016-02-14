from django.contrib import admin

from dream.core.models import Club, Team


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'modified',
        'manager',
        'country'
    )
    search_fields = [
        'name',
        'country__name',
        'country__country_code',
    ]

    class TeamInline(admin.TabularInline):
        model = Team

    inlines = [
        TeamInline
    ]
