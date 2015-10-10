from .single_match import SingleMatch


class DebugMatch(SingleMatch):

    def debug_data(self):
        coords = []

        for team_key in self.board.team_keys():
            team = self.board.teams[team_key]
            coords += team.debug_getplayercoords()

        ball_position = self.board.grid_state().player_with_ball.current_position

        data = {
            'player_coordinates': coords,
            'ball_coordinates': ball_position
        }

        return data
