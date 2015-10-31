from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _

from dream.tools import Logger
from dream.engine.soccer.service import SimulationService
from dream.engine.soccer.match.board import Board
from dream.core.models import Match
from dream.engine.soccer.exceptions import InitError
from json import loads as json_decode


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
        self.info = {
            'journal': None,
            'last_state': None,
            'selected_state': None      # Current state displayed by the simulator
        }

    def initialize(self, tick_id=None):

        # TODO: Break here -> Allow a go_to_tick call to change initial tick?
        if tick_id is not None:
            self.go_to_tick(tick_id)

        self.tactics = self.sim_service.fetch_tactics(self.match)

        if self.match_log is not None:
            self.logger.log('LOAD EXISTING BOARD')
            board_state = self.info['last_state']['board']
            self.board = Board.load_state(board_state, self.tactics)
        else:
            self.logger.log('CREATE NEW BOARD')
            self.board = self.sim_service.create_board()
            self.sim_service.place_teams_on_board(self.board, self.tactics)

        if self.match.status < Match.STATUS_SIM_STARTED:
            self.match.status = Match.STATUS_SIM_STARTED
            self.match.save()

    def go_to_tick(self, tick_id):
        from dream.core.models import MatchLog

        filters = {'match': self.match}

        try:
            if tick_id != -1:
                filters['sim_last_tick_id'] = tick_id
                self.match_log = MatchLog.objects.get(**filters)
            else:
                self.match_log = MatchLog.objects\
                    .filter(**filters)\
                    .latest('sim_last_tick_id')

            self.info['journal'] = json_decode(self.match_log.journal)
            self.info['last_state'] = json_decode(self.match_log.last_saved_state)
        except ObjectDoesNotExist:
            raise InitError(_('Tick with id: {} does not exist for match_id: {}'
                            .format(tick_id, self.match.pk)))

    def go_to_last_tick(self):
        pass

    def next_tick(self):
        # TODO: Go to tick that follows current state
        pass

    def previous_tick(self):
        # TODO: Go to tick that precedes current state
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

        gs = self.board.grid_state()
        teams = self.board.teams
        for team in teams.values():
            team.initialize(gs)

        self.logger.log('SIM STARTED')
