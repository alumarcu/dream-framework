from django.contrib import admin
from dream.engine.soccer.models import Requirement
from .inline import RequirementEnumValuesInline


@admin.register(Requirement)
class RequirementAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'type',
    )
    search_fields = ['name']
    list_filter = ('type', )
    inlines = [
        RequirementEnumValuesInline
    ]
