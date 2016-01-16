from django.db import models as _m
from django.utils.translation import ugettext_lazy as _

from .division import Division
from .board_template import BoardTemplate


class Match(_m.Model):
    """
    A match is part of a division and can have teams playing it.
    It may be part of a division's round and season. All teams
    should be registered to the division the game is part of
    """
    STATUS_SCHEDULED = 1
    STATUS_SIM_STARTED = 11
    STATUS_SIM_IN_PROGRESS = 12
    STATUS_SIM_FINISHED = 13
    STATUS_RENDER_STARTED = 22
    STATUS_RENDER_IN_PROGRESS = 23
    STATUS_RENDER_FINISHED = 23

    division = _m.ForeignKey(Division)

    round = _m.IntegerField(null=True, blank=True)

    season = _m.IntegerField(null=True, blank=True)

    can_be_draw = _m.BooleanField(default=True)

    # TODO: [MOD-03] Build a specialized class for stadiums
    # This should minimally know about name and capacity
    stadium = _m.IntegerField(null=True, blank=True)

    # Tells whether simulation or rendering is currently running
    status = _m.PositiveSmallIntegerField(default=1)

    # Number of minutes passed during rendering
    render_progress = _m.PositiveSmallIntegerField(null=True, blank=True)

    date_scheduled = _m.DateTimeField(_('scheduled on'), blank=True, null=True)

    ticks_per_minute = _m.PositiveSmallIntegerField(_('match ticks per minute'), default=10)
    board_template = _m.ForeignKey(BoardTemplate)

    created = _m.DateTimeField(auto_now_add=True)
    modified = _m.DateTimeField(auto_now=True)

    def __str__(self):
        return 'id: %s' % self.pk

    class Meta:
        verbose_name_plural = _('matches')
