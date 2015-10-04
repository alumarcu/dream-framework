from dream.engine.soccer.tools import engine_params


class GridState:
    ACTION_STATUS_PLAY_INTERRUPTED = 'play_interrupted'
    ACTION_STATUS_PLAY_ONGOING = 'play_ongoing'

    player_with_ball = None
    _action_status = None
    tick_id = None
    game_minute = None

    def __init__(self):
        self.tick_id = 0
        self.game_minute = 0
        self.ticks_per_minute = engine_params('match_ticks_per_minute')
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
        rules = engine_params(section='rules')
        mins = float(rules['match_minutes'])
        per = float(rules['match_periods'])
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

    def as_dict(self):
        data = {
            'action_status': self.action_status(),
            'tick_id': self.tick_id,
            'game_minute': self.game_minute,
            'player_with_ball': self.player_with_ball.id()
        }

        return data

    def from_dict(self, data, fp_cache, simulation):
        self.tick_id = data['tick_id']
        self.game_minute = data['game_minute']
        self.player_with_ball = fp_cache[data['player_with_ball']]
        self.action_status(data['action_status'])
        self.ticks_per_minute = simulation.log.sim_ticks_per_minute
