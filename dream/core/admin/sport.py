from django.contrib import admin

from dream.core.models import Sport


@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'common_key'
    )
    search_fields = [
        'name'
    ]
