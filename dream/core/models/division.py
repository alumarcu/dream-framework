from django.db.models import Model, CharField, DateTimeField, ForeignKey, SmallIntegerField
from django.utils.translation import ugettext_lazy as _

from . import League


class Division(Model):
    league = ForeignKey(League)

    level = SmallIntegerField(_('division level'))
    teams_num = SmallIntegerField(_('teams required'))

    name = CharField(_('division name'), max_length=30)

    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
