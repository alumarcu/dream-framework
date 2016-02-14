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

    def kickoff_xy(self, team_key):
        """
        Where the two players that kick the ball to start
        the game are placed in the beginning of the game
        :param team_key:
        :rtype list
        :return:
        """
        player_1 = player_2 = None

        if team_key == 'home':
            player_1 = (round(self.width() / 2), round(self.height() / 2))
            player_2 = (round(self.width() / 2) + 1, round(self.height() / 2))

        elif team_key == 'away':
            player_1 = (round(self.width() / 2) + 1, round(self.height() / 2) + 1)
            player_2 = (round(self.width() / 2), round(self.height() / 2) + 1)

        coords = [player_1, player_2]

        return coords

    class Meta:
        verbose_name_plural = _('board templates')
