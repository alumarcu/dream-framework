from dream.engine.soccer.tools import engine_params

from dream.engine.soccer.match.board.grid_state import GridState
from dream.engine.soccer.match.board.grid_cell import GridCell


class Grid:
    """
    :type template: dream.core.models.BoardTemplate
    :type state: dream.engine.soccer.match.board.GridState
    :type matrix: list[list[dream.engine.soccer.match.]
    """

    def __init__(self):
        self.template = None
        self.state = None
        self.matrix = []

    def initialize(self, template=None):
        """
        Called when the board is initialized or resumed
        :type template: dream.core.models.BoardTemplate
        :return:
        """
        self.template = template

        self.state = GridState()

        # Create one grid cell and contain the pitch as a matrix
        self.matrix = [[GridCell(self, w, l) for w in range(self.template.width())]
                       for l in range(self.template.height())]

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

    def export(self):
        """
        Exports non-empty cells of the game matrix
        :return:
        """
        data = {
            'matrix': [gc.export()
                       for g_row in self.matrix
                       for gc in g_row if len(gc.export()) > 0]
        }

        return data

    def resume(self, matrix, fp_cache):
        for celldata in matrix:
            cell = self.get_cell(celldata['xy'])
            if 'has_ball' in celldata:
                cell.has_ball = True
            if 'players' in celldata:
                # Load players
                for player_id in celldata['players']:
                    field_player = fp_cache[player_id]
                    field_player.current_position = celldata['xy']
                    self.place_player(fp_cache[player_id])

                if 'player_with_ball' in celldata:
                    self.give_ball_to(fp_cache[celldata['player_with_ball']])

        return self
