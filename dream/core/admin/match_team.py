from django.contrib import admin

from dream.core.models import MatchTeam


@admin.register(MatchTeam)
class MatchTeamAdmin(admin.ModelAdmin):
    list_display = (
        'team',
        'role',
        'tactics',
        'tactics_ref'
    )
