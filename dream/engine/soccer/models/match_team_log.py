from django.db import models as _m
from django.utils.translation import ugettext_lazy as _

from dream.core.models import MatchTeam, MatchLog


class MatchTeamLog(_m.Model):
    match_team = _m.ForeignKey(MatchTeam)

    match_log = _m.ForeignKey(MatchLog)

    # General phase of play
    action_phase = _m.CharField(_('phase of action'), max_length=30)

    # Phase of set pieces or sub-phase
    resume_phase = _m.CharField(_('phase after interruption'), max_length=30)

    kick_off = _m.BooleanField(_('had kick off'))

    players = _m.TextField(blank=True)
