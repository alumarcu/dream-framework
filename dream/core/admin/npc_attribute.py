from django.contrib import admin

from dream.core.models import NpcAttribute


@admin.register(NpcAttribute)
class NpcAttributeAdmin(admin.ModelAdmin):
    list_display = (
        'npc',
        'attribute',
        'value'
    )
    search_fields = [
        'attribute__name'
    ]
