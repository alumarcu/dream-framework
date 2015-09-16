from django.db.models import Model, CharField, DateTimeField, \
    ForeignKey, SmallIntegerField
from django.utils.translation import ugettext_lazy as _

from dream.core.definitions import GENDER_CHOICES, GENDER_UNDEFINED
from . import Club, Team


class Npc(Model):
    """
    Can be players, staff of a club; or anyone else who
    may have a role in the overall game;
    has a gender; may or may not belong to a club,
    may be in a club but not in a team (e.g. staff)
    """
    club = ForeignKey(Club, blank=True, null=True)
    team = ForeignKey(Team, blank=True, null=True)

    first_name = CharField(_('npc first name'), max_length=15)
    last_name = CharField(_('npc last name'), max_length=15)
    nickname = CharField(_('npc nickname'), max_length=20, blank=True)

    age = SmallIntegerField(blank=True, null=True)
    gender = CharField(
        _('gender'),
        max_length=1,
        choices=GENDER_CHOICES,
        default=GENDER_UNDEFINED
    )

    # TODO: [MOD-04] NPC roles should be formalized in a
    # separate table; also see MOD-01
    # It should be possible to extract the sport(s)
    # the Npc is relevant to from his role
    role = CharField(_('role'), max_length=20, blank=True)

    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)

    def __str__(self):
        if self.nickname != '':
            return '%s "%s" %s' % (
                self.first_name,
                self.nickname,
                self.last_name
            )
        return '%s %s' % (self.first_name, self.last_name)
