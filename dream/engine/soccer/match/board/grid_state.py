from dream.engine.soccer.tools import engine_params


class GridState:
    """
    :type player_with_ball: dream.engine.soccer.match.actors.FieldPlayer
    """

    ACTION_STATUS_PLAY_INTERRUPTED = 'play_interrupted'
    ACTION_STATUS_PLAY_ONGOING = 'play_ongoing'

    player_with_ball = None
    _action_status = None
    tick_id = None
    game_minute = None

    def __init__(self):
        self.tick_id = 0
        self.game_minute = 0
        self._action_status = self.ACTION_STATUS_PLAY_INTERRUPTED

    def tick(self, new_tick=False):
        if new_tick is True:
            self.tick_id += 1
            if self.tick_id % 10 == 0:
                self.game_minute += 1
        return self.tick_id

    def action_status(self, action_status=None):
        if action_status is not None:
            self._action_status = action_status
        return self._action_status

    def period(self):
        # TODO: Extend this rudimentary implementation that does not account for Extra Time
        # TODO: Remove hardcode, store these in a set of rules (youth may play 80 min games)
        mins = 90
        per = 45
        # TODO: Improve this! It assumes there are only two periods always, will not work for
        # TODO: any given X minutes and Y periods
        if self.game_minute <= (mins / per):
            return 1
        elif self.game_minute <= mins:
            return 2

    def filters(self):
        return {
            'Game': {
                'ActionStatus': self.action_status(),
                'TickId': self.tick_id,
            }
        }
