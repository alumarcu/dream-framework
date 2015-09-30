from . import MoveAction


class OffensivePositionAction(MoveAction):

    def perform(self, player, board):
        print("-------------------------------")
        print(player.current_position)
        print(player.field_zone)

        grid = board.grid
        curr_coords = player.current_position
        coords = (curr_coords[0], curr_coords[1] + 15)   # Advance on y-pos

        print("%s moves to %s" % (player, coords))
        grid.move_player(player, coords)
