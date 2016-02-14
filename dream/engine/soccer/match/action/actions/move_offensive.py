from . import MoveAction


class OffensivePositionAction(MoveAction):

    def perform(self):
        print("-------------------------------")
        print(self.player.current_position)
        print(self.player.field_zone)

        grid = self.board.grid
        curr_coords = self.player.current_position
        coords = (curr_coords[0], curr_coords[1] + 15)   # Advance on y-pos

        print("%s moves to %s" % (self.player, coords))
        grid.move_player(self.player, coords)
