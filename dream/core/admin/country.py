from django.contrib import admin
from dream.core.models import Country


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'country_code',
        'id',
    )
    search_fields = [
        'name',
        'country_code',
    ]
