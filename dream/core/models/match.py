from django.db.models import Model, DateTimeField, ForeignKey, \
    IntegerField, PositiveSmallIntegerField, BooleanField
from django.utils.translation import ugettext_lazy as _

from . import Division


class Match(Model):
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

    division = ForeignKey(Division)

    round = IntegerField(null=True, blank=True)
    season = IntegerField(null=True, blank=True)
    can_be_draw = BooleanField(default=True)

    # TODO: [MOD-03] Build a specialized class for stadiums
    # This should minimally know about name and capacity
    stadium = IntegerField(null=True, blank=True)

    # Tells whether simulation or rendering is currently running
    status = PositiveSmallIntegerField(default=1)

    # Number of minutes passed during rendering
    render_progress = PositiveSmallIntegerField(null=True, blank=True)

    date_scheduled = DateTimeField(_('scheduled on'), blank=True, null=True)
    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)

    def __str__(self):
        return 'id: %s' % self.pk

    class Meta:
        verbose_name_plural = _('matches')
