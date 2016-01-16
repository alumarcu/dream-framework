from django.utils.translation import ugettext_lazy as _
from django.db.models import Model, CharField, SmallIntegerField


class FieldZone(Model):
    """
    A zone in the simulation board (i.e. CD1, FW1, etc.)
    """
    code = CharField(_('zone code'), max_length=5)
    row = SmallIntegerField(default=0)
    col = SmallIntegerField(default=0)

    def xy(self):
        from .field_zone_xy import FieldZoneXy
        return FieldZoneXy.objects.get(zone=self)
