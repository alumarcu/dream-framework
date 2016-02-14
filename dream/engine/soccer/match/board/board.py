from django.utils.translation import ugettext_lazy as _

from dream.tools import Logger
from dream.engine.soccer.exceptions import InitError
from dream.engine.soccer.tools import engine_params, simulation_log_message
from dream.engine.soccer.match.board.grid import Grid


class Board:
    """
    :type template: dream.core.models.BoardTemplate
    :type grid: dream.engine.soccer.match.board.grid.Grid
    :type teams: dict[string, dream.engine.soccer.match.actors.FieldTeam]
    """
    def __init__(self, template):
        self.template = template
        self.grid = Grid()

        self.teams = {}
        self.logger = Logger(__name__, simulation_log_message)

    def initialize(self):
        self.grid.initialize(template=self.template)
        self.initialize_teams()

    def log(self, message, level=Logger.LEVEL_DEBUG, **kwargs):
        kwargs['simtime'] = (self.grid_state().game_minute, self.grid_state().tick_id)
        self.logger.log(message, level, **kwargs)
        return '[DEBUG][M:{min:03d}_T:{tick:04d}] {msg}'.format(
            min=self.grid_state().game_minute,
            tick=self.grid_state().tick_id,
            msg=message
        )

    def initialize_teams(self):
        # TODO: TBD Below. Always should consider a team as home and one as away
        # TODO: 'home' and 'away' should be renamed to top and bottom (and define as constants),
        # TODO: since there will be a toss of coin for the field [ home = top, bottom = away ]
        self.teams = {
            'home': None,
            'away': None,
        }

    def export(self):
        data = {}
        data.update(self.grid.export())

        # for team_key in self.teams:
        # data['teams'].update(self.teams[team_key].export())

        return data

    def team_keys(self):
        return [key for key in self.teams.keys()]

    def create_field_team(self, match_team):
        """
        :param team_key:
        :type team_key:
        :return:
        :rtype: dream.engine.soccer.match.actors.FieldTeam
        """
        from dream.engine.soccer.match.actors import FieldTeam
        self.teams[match_team.role] = FieldTeam(match_team)
        return self.teams[match_team.role]

    def place_player_on_field(self, field_player):
        # TODO: Move this method into field_player class
        from dream.engine.soccer.match.actors import FieldPlayer

        if not isinstance(field_player, FieldPlayer):
            message = _('Only FieldPlayer objects can be placed on field')
            raise InitError(message)

        # TODO: This is bugged and should be fixed later
        raise NotImplementedError('Fix player_player_on_field zone calculation!')
        zone_center = self.zones[field_player.field_zone][field_player.team.key() + '_center']

        field_player.init_start_position(zone_center, self.grid)

    def grid_state(self):
        return self.grid.state
