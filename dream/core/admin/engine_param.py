from django.contrib import admin
from dream.core.models import EngineParam


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
