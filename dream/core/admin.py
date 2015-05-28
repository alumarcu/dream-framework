from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from dream.core.models import *


# TODO: [ADM-01] Customize admin classes
admin.site.register(Country)
admin.site.register(League)
admin.site.register(Attribute)
admin.site.register(Sport)
admin.site.register(Division)
admin.site.register(Club)
admin.site.register(Manager)
admin.site.register(ManagerAttribute)
admin.site.register(Npc)
admin.site.register(NpcAttribute)
admin.site.register(Team)


class MatchStatusFilter(admin.SimpleListFilter):
    """
    Allows filtering matches by their status in the admin interface
    """
    title = _('Status')
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return (
            (Match.STATUS_SCHEDULED, _('Scheduled')),
            (Match.STATUS_SIM_STARTED, _('Sim Started')),
            (Match.STATUS_SIM_IN_PROGRESS, _('Sim In Progress')),
            (Match.STATUS_SIM_FINISHED, _('Sim Finished')),
            (Match.STATUS_RENDER_STARTED, _('Render Started')),
            (Match.STATUS_RENDER_IN_PROGRESS, _('Render In Progress')),
            (Match.STATUS_RENDER_FINISHED, _('Render Finished')),
        )

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(status=self.value())


# TODO: [ADM-02] Improve existing admin classes
# Several entities should be defined inline inside others
# see: https://docs.djangoproject.com/en/1.8/intro/tutorial02/
@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = (
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


@admin.register(MatchTeam)
class MatchTeamAdmin(admin.ModelAdmin):
    list_display = (
        'team',
        'role',
        'tactics',
        'tactics_ref'
    )
