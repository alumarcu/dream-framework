from json import loads as json_decode
from dream.tools import Logger
from dream.engine.soccer.service import SimulationService
from dream.engine.soccer.match import Ticker
from dream.core.models import Match


class ManualMatch:
    """
    A match that is played step-by-step for debugging purposes
    """
    def __init__(self, match_id):
        self.logger = Logger(__name__, Logger.default_message)
        self.match = Match.objects.get(pk=match_id)
        self.sim_service = SimulationService()
        self.match_log = None
        self.tactics = None
        self.board = None
        self.ticker = None
        self.info = {
            'journal': None,
            'last_state': None
        }

    def initialize(self, tick_id=None):
        self.tactics = self.sim_service.fetch_tactics(self.match)

        if tick_id is not None:
            self.go_to_tick(tick_id)

        else:
            self.board = self.sim_service.create_board(self.tactics)
            self.ticker = Ticker(self.board)

            self.match.status = Match.STATUS_SIM_STARTED
            self.match.save()

    def go_to_tick(self, tick_id):
        self.board, self.match_log, last_state = self.sim_service\
            .resume_board(self.match, tick_id, self.tactics)

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
        # TODO: Save new state

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

        gs = self.board.grid_state()
        teams = self.board.teams
        for team in teams.values():
            team.initialize(gs)

        self.logger.log('SIM STARTED')
