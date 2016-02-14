from . import PassAction


class IndirectKickPassAction(PassAction):

    def perform(self):
        print("-------------------------------")
        print(self.player.current_position)
        print(self.player.field_zone)

        grid = self.board.grid
        current_grid_cell = grid.get_cell(self.player.current_position)
        next_grid_cell = None

        if self.player.ROLE_FREE_KICKS in self.player.roles and self.player.team.kickoff_first:
            # TODO: Negate and quit OR validate

            print("The player kicks off the ball")
            kickoff_zones = grid.template.kickoff_xy(self.player.team.key())
            # Coords of the next grid cell
            next_position = kickoff_zones[1]
            next_grid_cell = grid.get_cell(next_position)

            self.move_ball(current_grid_cell, next_grid_cell)
