from django.db.models import Model, ForeignKey, CharField, SmallIntegerField, DateTimeField
from django.utils.translation import ugettext_lazy as _

from dream.core.definitions import GENDER_CHOICES, GENDER_UNDEFINED
from . import Country, Sport


class League(Model):
    """
    A league is defined by a country and a sport and
    contains a collection of divisions
    """
    country = ForeignKey(Country)
    sport = ForeignKey(Sport)

    name = CharField(_('league name'), max_length=60)

    min_age = SmallIntegerField(_('minimum age for signup'))
    max_age = SmallIntegerField(_('maximum age for signup'))

    gender = CharField(
        _('gender'),
        max_length=1,
        choices=GENDER_CHOICES,
        default=GENDER_UNDEFINED
    )

    # TODO: [MOD-02] A specialized class which handles calendars and schedules
    # should be created. The component should allow adding different schedules
    # for each country, league and sport.

    schedule = SmallIntegerField()

    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
