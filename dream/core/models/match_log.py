from django.db import models as _m
from django.utils.translation import ugettext_lazy as _

from . import Match


class MatchLog(_m.Model):

    match = _m.ForeignKey(Match)

    minute = _m.SmallIntegerField(_('simulation minutes passed'), default=0)

    tick = _m.IntegerField(_('last tick id'), default=0)

    ticks_per_min = _m.SmallIntegerField(_('simulation ticks per minute param'), default=0)

    # A JSON with data required to load the game state and resume after an interruption
    state = _m.TextField(blank=True)

    modified = _m.DateTimeField(_('modified'), auto_now=True)

    created = _m.DateTimeField(_('created'), auto_now_add=True)

    def __str__(self):
        return 'Log [match_id:{}, tick_id:{}]'.format(self.match.pk, self.tick)
