from django.contrib import admin

from dream.core.models import Attribute
from .filters import SportFilter, AttributeApplicabilityFilter, AttributeTypeFilter


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'sport',
        'applies_to',
        'modified',
        'type',
    )
    search_fields = [
        'name',
        'description',
    ]
    list_filter = (SportFilter, AttributeApplicabilityFilter, AttributeTypeFilter, )
