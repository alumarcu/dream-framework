from django.contrib import admin

from dream.core.models import ManagerAttribute


@admin.register(ManagerAttribute)
class ManagerAttributeAdmin(admin.ModelAdmin):
    list_display = (
        'manager',
        'attribute',
        'value',
    )
    search_fields = [
        'attribute__name'
    ]
