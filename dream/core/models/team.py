from django.db.models import Model, CharField, DateTimeField, ForeignKey
from django.utils.translation import ugettext_lazy as _

from dream.core.definitions import GENDER_CHOICES, GENDER_UNDEFINED
from . import Club


class Team(Model):
    club = ForeignKey(Club)

    name = CharField(_('team name'), max_length=60)
    gender = CharField(
        _('gender'),
        max_length=1,
        choices=GENDER_CHOICES,
        default=GENDER_UNDEFINED
    )

    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
