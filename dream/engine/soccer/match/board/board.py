from django.utils.translation import ugettext_lazy as _

from dream.tools import Logger
from dream.engine.soccer.exceptions import InitError
from dream.engine.soccer.tools import engine_params, simulation_log_message
from dream.engine.soccer.match.board.grid import Grid


class Board:
    def __init__(self):
        params = engine_params(section='tactics')

        self.rows = int(params['board_grid_rows'])
        self.cols = int(params['board_grid_cols'])
        self.grid = Grid()

        self.zones = None
        self.zone_len = None
        self.zone_width = None
        self.teams = {}

        self.logger = Logger(__name__, simulation_log_message)

    def initialize(self):
        self.grid.initialize()
        self.initialize_zones()
        self.initialize_teams()

    def log(self, message, level=Logger.LEVEL_DEBUG, **kwargs):
        kwargs['simtime'] = (self.grid_state().game_minute, self.grid_state().tick_id)
        self.logger.log(message, level, **kwargs)

    def initialize_teams(self):
        self.teams = {
            'home': None,
            'away': None,
        }

    def as_dict(self):
        data = {
            'rows': self.rows,
            'cols': self.cols,
            'zones': self.zones,
            'zone_len': self.zone_len,
            'zone_width': self.zone_width,
            'grid': self.grid.as_dict(),
            'teams': {}
        }
        for team_key in self.teams:
            data['teams'][team_key] = self.teams[team_key].as_dict()

        return data

    def from_dict(self, data, tactics):
        from dream.engine.soccer.match.actors import FieldTeam
        from dream.engine.soccer.service.simulation import SimulationService

        sim_service = SimulationService()
        self.rows = data['rows']
        self.cols = data['cols']

        self.zones = data['zones']
        self.zone_len = data['zone_len']
        self.zone_width = data['zone_width']

        for team_key in data['teams']:
            team = FieldTeam(team_key)
            team.field_players = sim_service.create_field_players(team, tactics)
            team.from_dict(data['teams'][team_key])
            self.teams[team_key] = team

        fp_cache = {}  # player IDs => FieldPlayer
        for team in self.teams.values():
            for fp in team.players():
                fp.team = team
                fp_cache[fp.id()] = fp

        self.grid = Grid().from_dict(data['grid'], fp_cache)

        return self

    @staticmethod
    def load_state(data, tactics):
        board = Board()
        return board.from_dict(data, tactics)

    def team_keys(self):
        return [key for key in self.teams.keys()]

    def create_field_team(self, team_key):
        from dream.engine.soccer.match.actors import FieldTeam
        self.teams[team_key] = FieldTeam(team_key)
        return self.teams[team_key]

    def initialize_zones(self):
        from dream.engine.soccer.models import FieldZone

        raw_zones = FieldZone.objects.all()
        self.zone_len = (self.grid.length / 2) / self.rows
        self.zone_width = self.grid.width / self.cols

        self.zones = {}
        for zone in raw_zones:
            self.zones[zone.code] = {
                'home_len': (
                    zone.row * self.zone_len - self.zone_len,
                    zone.row * self.zone_len),
                'home_width': (
                    zone.col * self.zone_width - self.zone_width,
                    zone.col * self.zone_width),
                'away_len': (
                    self.grid.length - (zone.row * self.zone_len - self.zone_len),
                    self.grid.length - (zone.row * self.zone_len)),
                'away_width': (
                    self.grid.width - (zone.col * self.zone_width - self.zone_width),
                    self.grid.width - (zone.col * self.zone_width)),
                }

            self.zones[zone.code]['home_center'] = self.get_zone_center(
                self.zones[zone.code]['home_width'],
                self.zones[zone.code]['home_len'])

            self.zones[zone.code]['away_center'] = self.get_zone_center(
                self.zones[zone.code]['away_width'],
                self.zones[zone.code]['away_len'])

    def place_player_on_field(self, field_player):
        from dream.engine.soccer.match.actors import FieldPlayer
        if type(field_player) is not FieldPlayer:
            message = _('Only FieldPlayer objects can be placed on field')
            raise InitError(message)

        zone_center = self.zones[field_player.field_zone][field_player.team.key() + '_center']

        field_player.init_start_position(zone_center, self.grid)

    def grid_state(self):
        return self.grid.state

    @staticmethod
    def get_zone_center(width, length):
        if (type(width) is not tuple) or (type(length) is not tuple):
            return
        return (
            round((width[0] + width[1]) / 2),
            round((length[0] + length[1]) / 2)
        )
