from django.contrib import admin

from dream.core.models import Npc, NpcAttribute


@admin.register(Npc)
class NpcAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'nickname',
        'id',
        'team',
        'club',
    )

    class NpcAttributeInline(admin.TabularInline):
        model = NpcAttribute

    inlines = [NpcAttributeInline]
