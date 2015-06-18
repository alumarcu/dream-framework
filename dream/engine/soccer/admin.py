from django.contrib import admin
from dream.engine.soccer.models import *


@admin.register(ActionRequirement)
class ActionRequirementAdmin(admin.ModelAdmin):
    list_display = (
        'edit',
        'action',
        'requirement',
        'condition',
        'value',
    )
    search_fields = [
        'action__name',
        'requirement__name'
    ]
    list_filter = ('action', 'condition',)

    def edit(self, obj):
        return 'Edit'

    edit.short_description = ''
    edit.admin_order_field = 'requirement__name'


@admin.register(EngineParam)
class EngineParamAdmin(admin.ModelAdmin):
    list_display = (
        'edit',
        'section',
        'key',
        'value',
        'description',
    )

    search_fields = [
        'section',
        'key',
        'description'
    ]
    list_filter = ('section',)

    def edit(self, obj):
        return 'Edit'

    edit.short_description = ''
    edit.admin_order_field = 'requirement__name'


@admin.register(FieldZone)
class FieldZoneAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'row',
        'col',
    )
    list_filter = ('row', 'col',)


@admin.register(PlayerAction)
class PlayerActionAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'enabled',
    )
    search_fields = ['name', 'description']
    list_filter = ('enabled',)


class RequirementEnumValuesInline(admin.TabularInline):
    model = RequirementEnumValue


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
