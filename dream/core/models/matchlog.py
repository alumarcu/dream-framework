from django.db.models import Model, DateTimeField, ForeignKey, \
    IntegerField, SmallIntegerField, TextField
from django.utils.translation import ugettext_lazy as _

from . import Match


class MatchLog(Model):
    match = ForeignKey(Match)

    sim_minutes_passed = SmallIntegerField(_('simulation minutes passed'), default=0)
    sim_last_tick_id = IntegerField(_('last tick id'), default=0)
    sim_ticks_per_minute = SmallIntegerField(_('simulation ticks per minute param'), default=0)

    last_modified = DateTimeField(auto_now=True)

    # A JSON with data required to load the game state and resume after an interruption
    last_saved_state = TextField(blank=True)

    # A JSON with data required to render the game after simulation
    journal = TextField(blank=True)