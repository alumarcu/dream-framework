from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from dream.core.models import Attribute


class AttributeTypeFilter(admin.SimpleListFilter):
    title = _('Type')
    parameter_name = 'type'

    def lookups(self, request, model_admin):
        return (
            (Attribute.ATTR_TYPE_TRAIT, _('%s - Trait' % Attribute.ATTR_TYPE_TRAIT)),
            (Attribute.ATTR_TYPE_SKILL, _('%s - Skill' % Attribute.ATTR_TYPE_SKILL)),
        )

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(type=self.value())
