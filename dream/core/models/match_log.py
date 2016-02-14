from django.db import models as _m
from django.utils.translation import ugettext_lazy as _

from . import Match, Npc


class MatchLog(_m.Model):

    match = _m.ForeignKey(Match, on_delete=_m.CASCADE)

    minute = _m.SmallIntegerField(_('simulation minutes passed'), default=0)

    tick = _m.IntegerField(_('last tick id'), default=0)

    action_status = _m.CharField(_('match action status'), blank=True, max_length=60)

    player_with_ball = _m.ForeignKey(Npc, on_delete=_m.CASCADE, null=True, blank=True,
                                     default=None)

    # A JSON with general data required to load the game state
    # and resume after an interruption, not including team states
    state = _m.TextField(blank=True)

    modified = _m.DateTimeField(_('modified'), auto_now=True)

    created = _m.DateTimeField(_('created'), auto_now_add=True)

    def __str__(self):
        return 'Log [match_id:{}, tick_id:{}]'.format(self.match.pk, self.tick)
