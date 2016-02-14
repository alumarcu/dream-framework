from django.contrib import admin

from dream.core.models import Team, Npc


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = (
        'club',
        'name',
        'gender',
        'modified',
    )
    search_fields = [
        'name'
        'club__name',
    ]

    class NpcInline(admin.TabularInline):
        model = Npc

    inlines = [
        NpcInline
    ]
