from django.db.models import Model, DateTimeField, ForeignKey, DecimalField
from django.utils.translation import ugettext_lazy as _

from .. import Manager, Attribute


class ManagerAttribute(Model):
    """
    Holds the attributes assigned to each manager and their respective values
    """
    manager = ForeignKey(Manager)
    attribute = ForeignKey(Attribute)

    value = DecimalField(
        _('value of the attribute'),
        max_digits=16,
        decimal_places=4
    )

    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)
