from django.utils.translation import ugettext_lazy as _
from django.db.models import Model, CharField, ForeignKey

from .requirement import Requirement
from .player_action import PlayerAction


class ActionRequirement(Model):
    """
    Correspondence between PlayerAction and Requirement;
    defines conditions under which a requirement applies to a value
    """
    CONDITION_IS = 'is'
    CONDITION_CAN_BE = 'can_be'
    CONDITION_ABOVE = 'above'
    CONDITION_ABOVE_OR_EQUAL = 'above_or_equal'
    CONDITION_BELOW = 'below'
    CONDITION_BELOW_OR_EQUAL = 'below_or_equal'

    action = ForeignKey(PlayerAction)
    requirement = ForeignKey(Requirement)

    condition = CharField(_('condition'), max_length=30)
    value = CharField(_('condition value'), max_length=250)
