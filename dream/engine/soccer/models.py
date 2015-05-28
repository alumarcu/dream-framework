from django.db.models import Model, CharField, BooleanField, ForeignKey, SmallIntegerField
from django.utils.translation import ugettext_lazy as _


class EngineParam(Model):
    section = CharField(_('section'), max_length=100, db_index=True)
    key = CharField(_('key'), max_length=250, unique=True, db_index=True)
    value = CharField(_('value'), max_length=250)
    description = CharField(_('description'), max_length=250, blank=True, default='')

    def __str__(self):
        return '%s.%s = %s' % (self.section, self.key, self.value)


class PlayerAction(Model):
    """
    Defines actions a FieldPlayer can perform during game
    """
    name = CharField(_('action name'), max_length=30)
    description = CharField(_('action description'), max_length=250, blank=True)
    # Whether the action can happen or is disabled
    enabled = BooleanField(_('action enabled'), default=False)

    def __str__(self):
        return self.name


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
    type = CharField('requirement type', max_length=10, choices=TYPES, default=TYPE_INT)

    def __str__(self):
        return self.name

    def enum_values(self, ids=None):
        if ids is None:
            return RequirementEnumValue.objects.filter(requirement=self)
        if type(ids) is int:
            ids = [ids]
        return RequirementEnumValue.objects.filter(pk__in=ids)


class RequirementEnumValue(Model):
    """
    Defines the allowed values of enum-type requirements
    """
    requirement = ForeignKey(Requirement)

    value = CharField(_('enum value'), max_length=30)

    def __str__(self):
        return '%s: %s' % (self.requirement.name, self.value)


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

    def parsed(self):
        requirement_type = self.requirement.type
        required_values = None

        if requirement_type == Requirement.TYPE_BOOL:
            required_values = True if self.value == Requirement.VAL_BOOL_TRUE else False
        elif requirement_type == Requirement.TYPE_INT:
            required_values = int(self.value)
        elif requirement_type == Requirement.TYPE_ENUM:
            from json import loads as json_decode

            # IDs of values that are required
            value_ids = json_decode(self.value)
            # Getting the actual values from IDs
            enum_values = self.requirement.enum_values(value_ids)
            # TODO: [SIM-08] Should check that all enum values have been found
            required_values = [ev.value for ev in enum_values]

        req_key = self.requirement.name
        req_data = {
            'condition': self.condition,
            'required_values': required_values,
        }

        return {req_key: req_data}


class FieldZone(Model):
    """
    A zone in the simulation board (i.e. CD1, FW1, etc.)
    """
    code = CharField('zone code', max_length=5)
    row = SmallIntegerField(default=0)
    col = SmallIntegerField(default=0)