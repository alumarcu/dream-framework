from django.db.models import Model, DecimalField, DateTimeField, ForeignKey
from django.utils.translation import ugettext_lazy as _

from .. import Npc, Attribute


class NpcAttribute(Model):
    npc = ForeignKey(Npc)
    attribute = ForeignKey(Attribute)

    value = DecimalField(
        _('value of the attribute'),
        max_digits=16,
        decimal_places=4
    )

    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)
