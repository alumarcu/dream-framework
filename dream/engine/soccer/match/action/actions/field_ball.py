from . import FieldAction


class BallAction(FieldAction):

    def move_ball(self, source_cell, target_cell):
        # Remove ball from player in the current grid cell
        source_cell.has_ball = None
        source_cell.player_with_ball.has_ball_action = False
        source_cell.player_with_ball = None

        target_cell.has_ball = True

        ball_winner = self.get_ball_winner(target_cell.players)
        if ball_winner is not False:
            target_cell.give_ball_to(ball_winner)

    def get_ball_winner(self, players_on_cell):
        if len(players_on_cell) == 0:
            return False
        # TODO --> Competition for ball between two players
        # in same cell, or just random
        return players_on_cell[0]
