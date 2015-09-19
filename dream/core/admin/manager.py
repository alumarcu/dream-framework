from django.contrib import admin

from dream.core.models import Manager, ManagerAttribute


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'user',
        'age',
        'gender',
        'modified',
    )
    search_fields = [
        'name',
        'user__first_name',
        'user__last_name',
        'user__email',
        'user__username'
    ]

    class ManagerAttributeInline(admin.TabularInline):
        model = ManagerAttribute

    inlines = [ManagerAttributeInline]
