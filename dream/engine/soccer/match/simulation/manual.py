from dream.tools import Logger
from dream.engine.soccer.service import SimulationService
from dream.engine.soccer.match.board import Board
from dream.core.models import Match
from json import loads as json_decode


class ManualMatch:
    """
    A match that is played step-by-step for debugging purposes
    """
    def __init__(self, match_id):

        self.logger = Logger(__name__, Logger.default_message)
        self.match = Match.objects.get(pk=match_id)
        self.sim_service = SimulationService()
        self.logs = None
        self.tactics = None
        self.board = None
        self.info = {
            'journal': None,
            'last_state': None
        }

    def initialize(self, up_to_tick=None):
        from dream.core.models import MatchLog
        filters = {'match': self.match}
        if up_to_tick is not None:
            filters['sim_last_tick_id__lte'] = up_to_tick

        self.logs = MatchLog.objects\
            .filter(**filters)\
            .order_by('-sim_last_tick_id')

        if len(self.logs) > 0:
            last_tick = self.logs[0]

            self.info['journal'] = json_decode(last_tick.journal)
            self.info['last_state'] = json_decode(last_tick.last_saved_state)

        self.tactics = self.sim_service.fetch_tactics(self.match)
        if self.info['last_state'] is None:
            self.board = self.sim_service.create_board()
            self.sim_service.place_teams_on_board(self.board, self.tactics)
        else:
            board_state = self.info['last_state']['board']
            self.board = Board.load_state(board_state, self)

        if self.match.status < Match.STATUS_SIM_STARTED:
            self.match.status = Match.STATUS_SIM_STARTED
            self.match.save()

    def go_to_tick(self, tick_id):
        pass

    def next_tick(self):
        pass

    def previous_tick(self):
        pass

    def create_tick(self):
        """
        Computes new tick after the last known tick
        :return:
        """
        pass

    def delete_ticks_from(self, tick_id):
        """
        Will delete all ticks following and including a given tick_id
        :param tick_id:
        :return:
        """
        pass

    def begin_simulation(self):
        if self.match.status < Match.STATUS_SIM_IN_PROGRESS:
            self.match.status = Match.STATUS_SIM_IN_PROGRESS
            self.match.save()

        gs = self.board.grid_sate()
        teams = self.board.teams
        for team in teams.values():
            team.initialize(gs)

        self.logger.log('SIM STARTED')
