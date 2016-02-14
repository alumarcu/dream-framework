from django.contrib import admin
from dream.engine.soccer.models import FieldZone


@admin.register(FieldZone)
class FieldZoneAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'row',
        'col',
    )
    list_filter = ('row', 'col',)
