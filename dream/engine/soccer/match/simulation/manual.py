from json import dumps as json_encode
from dream.tools import Logger
from dream.engine.soccer.service import SimulationService
from dream.engine.soccer.match import Ticker
from dream.core.models import Match


class ManualMatch:
    """
    A match that is played step-by-step for debugging purposes
    :type ticker    dream.engine.soccer.match.Ticker
    :type board     dream.engine.soccer.match.board.Board
    """
    def __init__(self, match_id):
        self.logger = Logger(__name__, Logger.default_message)
        self.match = Match.objects.get(pk=match_id)
        self.sim_service = SimulationService(self.match)
        self.match_log = None
        self.board = None
        self.ticker = None
        self.info = {
            'journal': None,
            'last_state': None
        }

    def initialize(self, tick_id=None):
        if tick_id is not None:
            self.go_to_tick(tick_id)

        else:
            self.board = self.sim_service.create_board()
            self.ticker = Ticker(self.board)

            self.match.status = Match.STATUS_SIM_STARTED
            self.match.save()

    def go_to_tick(self, tick_id):
        self.board, self.match_log, last_state = self.sim_service.resume_board(tick_id)

        self.ticker = Ticker(self.board)
        self.info['last_state'] = last_state

    def next_tick(self):
        tick_id = self.match_log.tick
        self.go_to_tick(tick_id + 1)

    def previous_tick(self):
        tick_id = self.match_log.tick
        self.go_to_tick(tick_id - 1)

    def create_tick(self):
        """
        Computes new tick after the last known tick
        :return:
        """
        # Create the new tick id using a tick mechanics class
        self.ticker.perform()

        # Save new state
        from dream.core.models.match_log import MatchLog
        gs = self.board.grid_state()
        exported_board = self.board.export()
        state = exported_board['matrix']

        ## TODO: This should be in a transaction

        ml = MatchLog(match=self.match)
        ml.minute = gs.game_minute
        ml.tick = gs.tick_id
        ml.state = json_encode(state, separators=(',', ':'))
        ml.player_with_ball = gs.player_with_ball.npc
        ml.action_status = gs.action_status()
        # TODO: Move this somewhere where data from the start of match is stored
        # ticks_per_min should always remain the same as at start of match
        # Save the new match log
        ml.save()

        from dream.engine.soccer.models import MatchTeamLog

        # Create match team logs
        for field_team in self.board.teams.values():

            mtl = MatchTeamLog()
            mtl.match_team = field_team.match_team
            mtl.match_log = ml
            mtl.action_phase = field_team.action_phase
            mtl.resume_phase = field_team.resume_phase
            mtl.kick_off = field_team.kickoff_first

            players_list = []
            for player in field_team.field_players:
                players_list.append(player.export())

            mtl.players = json_encode(players_list)
            mtl.save()

            # TODO: ==== THIS IS THE LAST EDITED LINE ===
            # TODO: Code cleanup & testing before commit + code review

    def begin_simulation(self):
        if self.match.status < Match.STATUS_SIM_IN_PROGRESS:
            self.match.status = Match.STATUS_SIM_IN_PROGRESS
            self.match.save()

        gs = self.board.grid_state()
        teams = self.board.teams
        for team in teams.values():
            team.initialize(gs)

        self.logger.log('SIM STARTED')

    def match_info(self):
        coordinates = []
        for team_key in self.board.team_keys():
            team = self.board.teams[team_key]
            coordinates += team.match_info_get_player_coordinates()

        ball_position = self.board.grid_state().player_with_ball.current_position

        data = {
            'player_coordinates': coordinates,
            'ball_coordinates': ball_position
        }

        return data

    def last_tick_info(self):
        return self.ticker.get_log()
