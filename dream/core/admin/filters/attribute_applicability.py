from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from dream.core.models import Attribute


class AttributeApplicabilityFilter(admin.SimpleListFilter):
    title = _('Applies to')
    parameter_name = 'applies_to'

    def lookups(self, request, model_admin):
        return (
            (Attribute.APPLIES_TO_MANAGER, _('Manager')),
            (Attribute.APPLIES_TO_NPC, _('NPC')),
        )

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(applies_to=self.value())
