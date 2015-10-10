from django.contrib import admin
from dream.engine.soccer.models import PlayerAction


@admin.register(PlayerAction)
class PlayerActionAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'enabled',
    )
    search_fields = ['name', 'description']
    list_filter = ('enabled',)
