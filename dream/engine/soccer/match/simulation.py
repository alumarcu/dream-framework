from django.utils.translation import ugettext_lazy as _
from json import loads as json_decode, dumps as json_encode
from dream.tools import toss_coin
from dream.engine.soccer.tools import engine_params
from dream.engine.soccer.exceptions import InitError, SimulationError


class Simulation:
    def __init__(self):
        self._match_ids = []

    # TODO: [SIM-02] Look into abstract classes in Python and decide whether its the case here
    # Possible example: http://zaiste.net/2013/01/abstract_classes_in_python/
    # Official docs: https://docs.python.org/3/library/abc.html
    def tactics_ok(self, tactics):
        # TODO: [SIM-01] Tactics validation
        return True

    def add_match(self, match_id):
        if type(match_id) is not int:
            raise InitError(_('Invalid match id supplied'))
        self._match_ids.append(match_id)

    def initialize(self):
        pass

    def loop(self):
        pass


class SingleMatch(Simulation):
    """
    Simulates a single soccer match
    """
    def __init__(self):
        super().__init__()
        self.match = None
        self.tactics = None
        self.board = None

    def initialize(self):
        self.match = self.init_match(self._match_ids[0])
        self.tactics = self.init_tactics()
        self.create_board()

        # TODO: [SIM-04] Advanced match status-related logic
        self.match.status = self.match.STATUS_SIM_STARTED
        self.match.save()

    def loop(self):
        game_rules = engine_params(section='rules')
        in_progress = True

        # TODO: [SIM-04] Advanced match status-related logic
        self.match.status = self.match.STATUS_SIM_IN_PROGRESS
        self.match.save()

        grid_state = self.board.grid_state()
        for team in self.board.teams.values():
            team.initialize(grid_state)

        print("The game is starting...")
        while in_progress:
            # TODO: Check if simulation is paused -> or if a tick should be made
            # this is a database value controlling the match, and is set async by browser
            self.tick(grid_state)
            break  # for now

        exit(_('Loop ended ok!'))

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
        from dream.engine.soccer.match.board import Board
        self.board = Board()
        self.board.initialize()

        # TODO: Board initialization on second half?

        # TODO: 'home' and 'away' should be renamed to top and bottom (and define as constants),
        # TODO: since there will be a toss of coin for the field [ home = top, bottom = away ]
        kickoff_team = toss_coin(self.board.team_keys())
        for team_key in self.board.team_keys():

            team = self.board.create_field_team(team_key)
            team.field_players = self.create_field_players(team)
            team.kickoff_first = True if team.key() == kickoff_team else False

            for player in team.field_players:
                self.board.place_player_on_field(player)

        print(self.board.grid.pretty_print())

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

    def tick(self, grid_state):
        grid_state.tick(new_tick=True)

        player_with_ball = grid_state.player_with_ball
        print("%s has the ball..." % player_with_ball)

        possible_actions = player_with_ball.get_possible_actions(grid_state.filters())
        print("Possible actions are: ", possible_actions)

        action = player_with_ball.decide_action(possible_actions)
        print("Decided action is: ", action)

        player_with_ball.perform_action(action, self.board)
        print("Action performed.")

        #print(self.board.grid.pretty_print())

        #exit("TODO: Process players without ball in this tick;")

        # Decide order of players

        players_to_move = []
        for team in self.board.teams.values():
            players_to_move += team.field_players

        players_to_move.remove(player_with_ball)

        players_to_move = self.players_move_order(players_to_move, player_with_ball.team.key())

        for player in players_to_move:
            # TODO: [SIM-05] A player from the opposing team should follow, check ordering
            # Actions available: advance, etc.

            print("%s has the next action..." % player)

            possible_actions = player.get_possible_actions(grid_state.filters())
            print("Possible actions are: ", possible_actions)

            if len(possible_actions) == 0:
                # TODO: [SIM-07] There should always be actions, this should be a fail-safe only
                break  # continue

            action = player_with_ball.decide_action(possible_actions)
            print("Decided action is: ", action)

            player_with_ball.perform_action(action, self.board)
            print("Action performed.")

            break

        print(self.board.grid.pretty_print())



    def players_move_order(self, players_list, kickoff_team):
        # TODO: [SIM-06] Better movement order based on INITIATIVE, DISTANCE TO BALL, TEAM, ETC
        from random import shuffle
        shuffle(players_list)
        return players_list

class DebugMatch(SingleMatch):
    def debug_data(self):
        coords = []

        for team_key in self.board.team_keys():
            team = self.board.teams[team_key]
            coords += team.debug_getplayercoords()

        data = {
            'player_coords': coords
        }

        return json_encode(data)
