from django.utils.translation import ugettext_lazy as _
from django.db.models import Model, CharField, ForeignKey

from .requirement import Requirement


class RequirementEnumValue(Model):
    """
    Defines the allowed values of enum-type requirements
    """
    requirement = ForeignKey(Requirement)

    value = CharField(_('enum value'), max_length=30)

    def __str__(self):
        return '%s: %s' % (self.requirement.name, self.value)
