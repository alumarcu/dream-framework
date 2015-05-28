from django.contrib import admin
from dream.engine.soccer.models import *


# TODO: [ADM-03] Customize admin classes
admin.site.register(EngineParam)
admin.site.register(PlayerAction)
admin.site.register(Requirement)
admin.site.register(RequirementEnumValue)
admin.site.register(ActionRequirement)
admin.site.register(FieldZone)
