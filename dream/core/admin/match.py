from django.contrib import admin

from dream.core.models import Match, MatchTeam
from .filters import MatchStatusFilter


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = (
        'edit',
        'id',
        'status',
        'division',
        'round',
        'season',
        'date_scheduled',
        'modified'
    )
    list_filter = (MatchStatusFilter, )
    search_fields = [
        'division__name',
        'division__league__name'
    ]

    def edit(self, obj):
        return 'Edit'

    edit.short_description = ''
    edit.admin_order_field = 'requirement__name'

    class MatchTeamInline(admin.TabularInline):
        model = MatchTeam

    inlines = [MatchTeamInline]
