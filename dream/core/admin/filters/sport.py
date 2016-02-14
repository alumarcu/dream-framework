from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from dream.core.models import Sport


class SportFilter(admin.SimpleListFilter):
    title = _('Sport')
    parameter_name = 'sport'

    def lookups(self, request, model_admin):
        return (
            (Sport.SPORT_SOCCER_KEY, _('Association Football')),
        )

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(sport__common_key=self.value())
