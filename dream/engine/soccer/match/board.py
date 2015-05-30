from django.utils.translation import ugettext_lazy as _
from dream.engine.soccer.tools import engine_params
from dream.engine.soccer.exceptions import InitError


class Board:
    def __init__(self):
        params = engine_params(section='tactics')

        self.rows = int(params['board_grid_rows'])
        self.cols = int(params['board_grid_cols'])
        self.grid = Grid()

        self.zones = None
        self.zone_len = None
        self.zone_width = None
        self.teams = None

    def initialize(self):
        self.grid.initialize()
        self.initialize_zones()
        self.initialize_teams()

    def initialize_teams(self):
        self.teams = {
            'home': None,
            'away': None,
        }

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


class Grid:
    width = None
    length = None
    matrix = None
    state = None

    def __init__(self):
        params = engine_params(section='pitch')

        self.width = int(params['grid_width'])
        self.length = int(params['grid_length'])

    def initialize(self):
        self.matrix = [[GridCell(self, w, l) for w in range(self.width)]
                       for l in range(self.length)]

        self.state = GridState()

    def pretty_print(self):
        ppgrid = ''
        for i in range(len(self.matrix)):
            line = ''
            for j in range(len(self.matrix[i])):
                line += str(self.matrix[i][j])
            ppgrid += line + "\n"
        return ppgrid

    def get_cell(self, coords):
        return self.matrix[coords[1]][coords[0]]

    def place_player(self, player):
        coords = player.current_position
        cell = self.matrix[coords[1]][coords[0]]
        cell.add_player(player)

    def move_player(self, player, new_coords):
        # Removed player from current position
        curr_coords = player.current_position
        curr_cell = self.matrix[curr_coords[1]][curr_coords[0]]
        curr_cell.remove_player(player)

        # Adding player to new location
        new_cell = self.matrix[new_coords[1]][new_coords[0]]
        new_cell.add_player(player)

    def give_ball_to(self, player):
        cell = self.get_cell(player.current_position)
        cell.give_ball_to(player)
        self.state.player_with_ball = player

    def get_kickoff_cell_coords(self, team_key):
        coords = []
        if team_key == 'home':
            coords = [
                (round(self.width / 2), round(self.length / 2)),
                (round(self.width / 2) + 1, round(self.length / 2)),
                ]
        elif team_key == 'away':
            coords = [
                (round(self.width / 2) + 1, round(self.length / 2) + 1),
                (round(self.width / 2), round(self.length / 2) + 1),
                ]
        return coords


class GridCell:

    def __init__(self, parent_grid, x_pos, y_pos):
        self.parent_grid = parent_grid
        self.players = []
        self.x_pos = x_pos
        self.y_pos = y_pos

        self.player_with_ball = None
        self.has_ball = None
        self.parent_zone = None  # TODO: A grid cell must know its zone and edge of the zone

    def add_player(self, player):
        self.players.append(player)

    def remove_player(self, player):
        self.players.remove(player)

    def has_players(self):
        return len(self.players) > 0

    def give_ball_to(self, player):
        if player in self.players:
            player.has_ball_action = True
            self.player_with_ball = player
            self.has_ball = True

    def __str__(self):
        if self.player_with_ball is not None:
            return '0'
        if self.has_players():
            return 'o'
        if self.has_ball:
            return '*'  # There's a ball here, but no player controls it
        if self.is_corner_edge() and self.is_oop_edge():
            return '+'
        if self.is_corner_edge():
            return '-'
        if self.is_oop_edge():
            return '|'

        return '.'

    def is_oop_edge(self):
        return self.x_pos == self.parent_grid.width - 1 or self.x_pos == 0

    def is_corner_edge(self):
        return self.y_pos == self.parent_grid.length - 1 or self.y_pos == 0


class GridState:
    ACTION_STATUS_PLAY_INTERRUPTED = 'play_interrupted'
    ACTION_STATUS_PLAY_ONGOING = 'play_ongoing'

    player_with_ball = None
    _action_status = None
    _tick_id = None
    _game_minute = None

    def __init__(self):
        self._tick_id = 0
        self._game_minute = 0
        self._action_status = self.ACTION_STATUS_PLAY_INTERRUPTED

    def tick(self, new_tick=False):
        if new_tick is True:
            self._tick_id += 1
        return self._tick_id

    def action_status(self, action_status=None):
        if action_status is not None:
            self._action_status = action_status
        return self._action_status

    def period(self):
        # TODO: Extend this rudimentary implementation that does not account for Extra Time
        rules = engine_params(section='rules')
        mins = float(rules['match_minutes'])
        per = float(rules['match_periods'])
        # TODO: Improve this! It assumes there are only two periods always, will not work for
        # TODO: any given X minutes and Y periods
        if self._game_minute <= (mins / per):
            return 1
        elif self._game_minute <= mins:
            return 2

    def filters(self):
        return {
            'Game': {
                'ActionStatus': self._action_status,
                'TickId': self._tick_id,
            }
        }
