from django.db import models as _m
from django.utils.translation import ugettext_lazy as _

from . import Match


class MatchJournal(_m.Model):
    match = _m.ForeignKey(Match)

    tick = _m.IntegerField(_('tickId'))

    # JSON reference for the entry (without i18n-processing)
    # contains all data required to render a sentence in the match report
    entry = _m.TextField(_('entry'), blank=True)

    modified = _m.DateTimeField(_('modified'), auto_now=True)

    created = _m.DateTimeField(_('created'), auto_now_add=True)
