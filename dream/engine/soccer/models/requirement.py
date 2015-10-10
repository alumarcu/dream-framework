from django.utils.translation import ugettext_lazy as _
from django.db.models import Model, CharField

from dream.engine.soccer.exceptions import LoopError


class Requirement(Model):
    """
    Defines requirements which can correspond to PlayerAction
    """
    TYPE_BOOL = 'bool'
    TYPE_INT = 'int'
    TYPE_ENUM = 'enum'
    TYPES = (
        (TYPE_BOOL, TYPE_BOOL),
        (TYPE_ENUM, TYPE_ENUM),
        (TYPE_INT, TYPE_INT),
    )
    # Definition of constant type values
    VAL_BOOL_TRUE = 'true'

    name = CharField('requirement name', max_length=30)
    type = CharField(
        'requirement type',
        max_length=10,
        choices=TYPES,
        default=TYPE_INT
    )

    def __str__(self):
        return self.name

    def enum_values(self, ids=None):
        from .requirement_enum_value import RequirementEnumValue

        if type(ids) in [list, int]:
            # Return values of certain IDs (or of a single ID)
            if type(ids) is int:
                ids = [ids]
            enum_values = RequirementEnumValue.objects.filter(pk__in=ids)
            if len(ids) != len(enum_values):
                raise LoopError(
                    _('Enum values missing for requirement: %s' % self.name))

        # Return all values for this requirement
        return RequirementEnumValue.objects.filter(requirement=self)
