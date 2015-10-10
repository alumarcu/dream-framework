from django.contrib import admin
from dream.engine.soccer.models import RequirementEnumValue


class RequirementEnumValuesInline(admin.TabularInline):
    model = RequirementEnumValue
