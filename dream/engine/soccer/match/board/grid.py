from dream.engine.soccer.tools import engine_params

from dream.engine.soccer.match.board.grid_state import GridState
from dream.engine.soccer.match.board.grid_cell import GridCell


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

    def as_dict(self):
        data = {
            'width': self.width,
            'length': self.length,
            'state': self.state.as_dict(),
            'matrix': [gc.as_dict()
                       for g_row in self.matrix
                       for gc in g_row if len(gc.as_dict()) > 0]
        }

        return data

    def from_dict(self, data, fp_cache, simulation):
        self.initialize()

        self.width = data['width']
        self.length = data['length']

        self.state.from_dict(data['state'], fp_cache, simulation)

        for celldata in data['matrix']:
            cell = self.get_cell(celldata['xy'])
            if 'has_ball' in celldata:
                cell.has_ball = True
            if 'players' in celldata:
                # load players
                for player_id in celldata['players']:
                    self.place_player(fp_cache[player_id])

                if 'player_with_ball' in celldata:
                    self.give_ball_to(fp_cache[celldata['player_with_ball']])

        return self
