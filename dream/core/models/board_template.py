from django.db import models as _m
from django.utils.translation import ugettext_lazy as _


class BoardTemplate(_m.Model):
    """
    Defines the format of the board
    """
    description = _m.CharField(_('description'), max_length=140, blank=True)

    rows = _m.PositiveSmallIntegerField(_('number of board rows'))

    cols = _m.PositiveSmallIntegerField(_('number of board zones'))

    zone_height = _m.PositiveSmallIntegerField(_('zone height (in cells)'))

    zone_width = _m.PositiveSmallIntegerField(_('zone width (in cells)'))

    def width(self):
        return self.cols * self.zone_width

    def height(self):
        return self.rows * self.zone_height

    class Meta:
        verbose_name_plural = _('board templates')
