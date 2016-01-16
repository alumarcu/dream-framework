from django.db import models as _m
from django.utils.translation import ugettext_lazy as _
from dream.core.models import BoardTemplate
from . import FieldZone


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

    class Meta:
        verbose_name_plural = _('field zone coordinates')

    def create_centers(self):
        """
        Creates centers for each zone, given valid height and width coordinates
        """
        self.home_center_x = round((self.home_xi + self.home_xj) / 2)
        self.home_center_y = round((self.home_yi + self.home_yj) / 2)

        self.away_center_x = round((self.away_xi + self.away_xj) / 2)
        self.away_center_y = round((self.away_yi + self.away_yj) / 2)
