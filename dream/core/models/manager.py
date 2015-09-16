from django.db.models import Model, CharField, DateTimeField, ForeignKey, SmallIntegerField
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from dream.core.definitions import GENDER_CHOICES, GENDER_UNDEFINED


class Manager(Model):
    """
    The manager represents the in-game Player Character and is
    bound directly to the User account. The evolution of PC is not
    bound to a sport but to a club which should contain all
    the assets which the PC is managing
    """
    user = ForeignKey(User)

    name = CharField(_('manager name'), max_length=60)
    age = SmallIntegerField(blank=True, null=True)
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
