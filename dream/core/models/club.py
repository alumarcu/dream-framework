from django.db.models import Model, CharField, DateTimeField, ForeignKey
from django.utils.translation import ugettext_lazy as _

from . import Manager, Country


class Club(Model):
    """
    Represents the collection of assets which the Manager manages in the game
    """
    manager = ForeignKey(Manager)
    country = ForeignKey(Country)

    name = CharField(_('club name'), max_length=60)

    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
