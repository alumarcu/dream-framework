from django.db.models import Model, CharField, DateTimeField, \
    ForeignKey, SmallIntegerField
from django.utils.translation import ugettext_lazy as _

from . import Sport


class Attribute(Model):
    """
    Defines attributes that can possibly apply to game
    entities, such as the Manager or NPCs.
    """
    ATTR_TYPE_TRAIT = 1     # A trait cannot be improved; it can only be gained or lost
    ATTR_TYPE_SKILL = 2     # A skill always exists with a certain level

    APPLIES_TO_MANAGER = 'manager'
    APPLIES_TO_NPC = 'npc'

    sport = ForeignKey(Sport)

    name = CharField(_('attribute name'), max_length=60)
    description = CharField(_('short description'), max_length=250)
    applies_to = CharField(max_length=10)
    type = SmallIntegerField(_('attribute type'), default=ATTR_TYPE_SKILL)

    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
