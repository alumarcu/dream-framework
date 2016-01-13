from django.db import models as _m
from django.utils.translation import ugettext_lazy as _
from . import FieldZone, BoardTemplate


class FieldZoneXy(_m.Model):
    zone = _m.ForeignKey(FieldZone)
    template = _m.ForeignKey(BoardTemplate)

    home_xi = _m.DecimalField(_('home x_1'), max_digits=12, decimal_places=4)
    home_xj = _m.DecimalField(_('home x_2'), max_digits=12, decimal_places=4)
    home_yi = _m.DecimalField(_('home y_1'), max_digits=12, decimal_places=4)
    home_yj = _m.DecimalField(_('home y_2'), max_digits=12, decimal_places=4)
    home_center_x = _m.DecimalField(_('home center x'), max_digits=12, decimal_places=4)
    home_center_y = _m.DecimalField(_('home center y'), max_digits=12, decimal_places=4)

    away_xi = _m.DecimalField(_('away x_1'), max_digits=12, decimal_places=4)
    away_xj = _m.DecimalField(_('away x_2'), max_digits=12, decimal_places=4)
    away_yi = _m.DecimalField(_('away y_1'), max_digits=12, decimal_places=4)
    away_yj = _m.DecimalField(_('away y_2'), max_digits=12, decimal_places=4)
    away_center_x = _m.DecimalField(_('away center x'), max_digits=12, decimal_places=4)
    away_center_y = _m.DecimalField(_('away center y'), max_digits=12, decimal_places=4)
