from django.contrib import admin
from dream.engine.soccer.models import ActionRequirement


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
