from . import PassAction


class IndirectKickPassAction(PassAction):

    def perform(self, player, board):
        print("-------------------------------")
        print(player.current_position)
        print(player.field_zone)

        grid = board.grid
        current_grid_cell = grid.get_cell(player.current_position)
        next_grid_cell = None

        if player.ROLE_FREE_KICKS in player.roles and \
                player.team.kickoff_first:
            # TODO: Negate and quit OR validate

            print("The player kicks off the ball")
            kickoff_zones = grid.get_kickoff_cell_coords(player.team.key())
            # Coords of the next grid cell
            next_position = kickoff_zones[1]
            next_grid_cell = grid.get_cell(next_position)

            self.move_ball(current_grid_cell, next_grid_cell)
