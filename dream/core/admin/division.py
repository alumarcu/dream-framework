from django.contrib import admin

from dream.core.models import Division, TeamDivision


@admin.register(Division)
class DivisionAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'league',
        'level',
        'teams_num',
        'modified',
    )
    search_fields = [
        'name',
        'league__name',
        'league__country__name',
        'league__country__country_code'
    ]

    class TeamDivisionInline(admin.TabularInline):
        model = TeamDivision

    inlines = [TeamDivisionInline]
