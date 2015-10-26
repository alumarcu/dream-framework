from django.utils.translation import ugettext_lazy as _
from json import loads as json_decode, dumps as json_encode

from dream.tools import toss_coin
from dream.engine.soccer.tools import engine_params
from dream.engine.soccer.match.board import Board
from dream.engine.soccer.exceptions import InitError, SimulationError
from dream.core.models import MatchLog

from .base import BaseSimulation


class SingleMatch(BaseSimulation):
    """
    Simulates a single soccer match
    """
    def __init__(self):
        super().__init__()
        self.match = None
        self.tactics = None
        self.board = None
        self.log = None
        self.saved_state = None
        self.journal = {}    # Will record the match journal

    def initialize(self):
        self.match = self.init_match(self._match_ids[0])

        # Get last match log entry for this match (if any)
        match_log = MatchLog.objects\
            .filter(match=self.match)\
            .order_by('-sim_minutes_passed', '-sim_last_tick_id')\
            .first()
        if type(match_log) is MatchLog:
            self.log = match_log
            # TODO: Error handling on invalid JSON
            self.journal = json_decode(match_log.journal)
            self.saved_state = json_decode(match_log.last_saved_state)

        self.tactics = self.init_tactics()
        self.board = self.load_board()

        # TODO: [SIM-04] Advanced match status-related logic
        # this will be initialized later
        self.match.status = self.match.STATUS_SIM_STARTED
        self.match.save()

    def init_match(self, match_id):
        """
        Returns an initialized Match object for the appropriate match
        """
        # TODO: [SIM-03] Check match status when simulation is initialized
        from dream.core.models import Match
        return Match.objects.get(pk=match_id)

    def init_tactics(self):
        from dream.core.models import MatchTeam
        match_teams = MatchTeam.objects.filter(match=self.match)
        tactics = {}
        for mt in match_teams:
            key = mt.role
            tactics[key] = self.decode_and_verify_tactics(mt.tactics)
        return tactics

    def decode_and_verify_tactics(self, tactics_data):
        try:
            decoded = json_decode(tactics_data)
            if self.tactics_ok(decoded):
                return decoded
        except InitError as ie:
            message = _('Invalid tactics in match_id %s : %s' % (self.match.pk, ie))
            raise InitError(message)
        except Exception as e:
            message = _('Error decoding tactics in match_id %s : %s' % (self.match.pk, e))
            raise SimulationError(message)

    def create_board(self):
        new_board = Board()
        new_board.initialize()

        # TODO: Board initialization on second half?

        # TODO: 'home' and 'away' should be renamed to top and bottom (and define as constants),
        # TODO: since there will be a toss of coin for the field [ home = top, bottom = away ]
        kickoff_team = toss_coin(new_board.team_keys())
        for team_key in new_board.team_keys():

            team = new_board.create_field_team(team_key)
            team.field_players = self.create_field_players(team)
            team.kickoff_first = True if team.key() == kickoff_team else False

            for player in team.field_players:
                new_board.place_player_on_field(player)

        return new_board

    def create_field_players(self, team):
        from dream.core.models import Npc, NpcAttribute
        from dream.engine.soccer.match.actors import FieldPlayer

        players = self.tactics[team.key()]['players']
        ids = [p['id'] for p in players]
        npcs = Npc.objects.filter(pk__in=ids)
        npc_attributes = NpcAttribute.objects.filter(npc__in=ids)

        field_players = []
        for player in players:
            fp = FieldPlayer()
            fp.npc = [npc for npc in npcs if npc.pk == int(player['id'])][0]
            fp.field_position = tuple(player['field_position'])
            fp.field_zone = player['field_zone']
            fp.attributes = [attr for attr in npc_attributes if attr.npc == int(player['id'])]
            fp.team = team
            fp.roles = player['roles'] if 'roles' in player else []
            field_players.append(fp)

        return field_players

    def loop(self):
        # game_rules = engine_params(section='rules')
        in_progress = True

        # TODO: [SIM-04] Advanced match status-related logic
        self.match.status = self.match.STATUS_SIM_IN_PROGRESS
        self.match.save()

        grid_state = self.board.grid_state()
        for team in self.board.teams.values():
            team.initialize(grid_state)

        self.logger.log('Game started.')
        while in_progress:
            # TODO: Check if simulation is paused -> or if a tick should be made
            # this is a database value controlling the match, and is set async by browser
            self.tick(grid_state)
            # TODO Save state to journal
            break  # for now

        # TODO: State of the match at startup
        new_state = self.save_state()
        new_state.save()

        # exit(_('Loop ended ok!'))

    def save_state(self):
        state = {'board': self.board.as_dict()}
        state_json = json_encode(state, separators=(',', ':'))

        new_log = MatchLog(match=self.match)
        new_log.sim_minutes_passed = self.board.grid_state().game_minute
        new_log.sim_last_tick_id = self.board.grid_state().tick_id
        new_log.sim_ticks_per_minute = engine_params(key='match_ticks_per_minute').value
        new_log.last_saved_state = state_json
        new_log.journal = self.journal

        return new_log

    def load_board(self):
        if self.saved_state is None:
            return self.create_board()

        board_state = self.saved_state['board']
        return Board.load_state(board_state, self)

    def tick(self, grid_state):
        grid_state.tick(new_tick=True)

        simtime = (grid_state.game_minute, grid_state.tick())

        player_with_ball = grid_state.player_with_ball
        self.board.log("%s has the ball." % player_with_ball)

        possible_actions = player_with_ball.get_possible_actions(grid_state.filters())
        self.board.log("Possible actions are: %s" % possible_actions)

        action = player_with_ball.decide_action(possible_actions)
        self.board.log("Decided action is: %s" % action)

        player_with_ball.perform_action(action, self.board)
        self.board.log("Action performed.")

        # print(self.board.grid.pretty_print())
        # exit("TODO: Process players without ball in this tick;")

        # Decide order of players
        players_to_move = []
        for team in self.board.teams.values():
            players_to_move += team.field_players

        players_to_move.remove(player_with_ball)

        players_to_move = self.players_move_order(players_to_move, player_with_ball.team.key())

        for player in players_to_move:
            # TODO: [SIM-05] A player from the opposing team should be next, check ordering
            # Actions available: advance, etc.

            self.logger.log("%s has the next action." % player, simtime=simtime)

            possible_actions = player.get_possible_actions(grid_state.filters())
            self.logger.log("Possible actions are: %s" % possible_actions, simtime=simtime)

            if len(possible_actions) == 0:
                # TODO: [SIM-07] There should always be actions, this should be a fail-safe only
                break  # continue

            action = player_with_ball.decide_action(possible_actions)
            self.logger.log("Decided action is: %s" % action, simtime=simtime)

            player_with_ball.perform_action(action, self.board)
            self.logger.log("Action performed.", simtime=simtime)

            break

        # print(self.board.grid.pretty_print())

    def players_move_order(self, players_list, kickoff_team):
        # TODO: [SIM-06] Better movement order based on INITIATIVE, DISTANCE TO BALL, TEAM, ETC
        from random import shuffle
        shuffle(players_list)
        return players_list
