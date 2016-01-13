from django.db import models as _m
from django.utils.translation import ugettext_lazy as _


class BoardTemplate(_m.Model):
    """
    Defines the format of the board
    """
    rows = _m.PositiveSmallIntegerField(_('number of board rows'))
    cols = _m.PositiveSmallIntegerField(_('number of board zones'))
    zone_height = _m.PositiveSmallIntegerField(_('zone height (in cells)'))
    zone_width = _m.PositiveSmallIntegerField(_('zone width (in cells)'))
