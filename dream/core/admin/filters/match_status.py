from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from dream.core.models import Match


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
