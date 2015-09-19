from django.contrib import admin

from dream.core.models import League, Division
from .filters import SportFilter


@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'country',
        'sport',
        'min_age',
        'max_age',
        'gender',
        'modified',
    )
    search_fields = [
        'name',
        'country__name',
        'country__country_code',
        'sport',
    ]
    list_filter = ('gender', SportFilter)

    class DivisionsInline(admin.TabularInline):
        model = Division

    inlines = [DivisionsInline]
