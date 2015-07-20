from django.utils.translation import ugettext_lazy as _
from dream.engine.soccer.exceptions import InitError, LoopError


class FieldTeam:
    PHASE_OFFENSIVE = 'phase_offensive'
    PHASE_BUILDPLAY = 'phase_buildplay'
    PHASE_COUNTERATTACK = 'phase_counterattack'
    PHASE_PRESSING = 'phase_pressing'
    PHASE_DEFENSIVE = 'phase_defensive'

    SP_FREEKICK = 'setpieces_freekick'
    SP_CORNER = 'setpieces_corner'
    SP_THROWIN = 'setpieces_throwin'
    SP_GOALKICK = 'setpieces_goalkick'
    SP_KICKOFF = 'setpieces_kickoff'
    SP_INDIRECT_FREEKICK = 'setpieces_indirectfreekick'
    SP_NONE = 'setpieces_none'

    _team_key = None
    _grid_state = None
    _team_phase = None
    _set_pieces = None

    def __init__(self, team_key):
        self._team_key = team_key

        self.kickoff_first = None
        self.field_players = []

    def key(self):
        return self._team_key

    def initialize(self, grid_state):
        self._grid_state = grid_state
        self.init_phase()

    def init_phase(self):
        # TODO: [ACT-01] Phase of play should change based on
        # which third is the ball in
        # and to whom it belongs as well as individual team tactics

        if (self.kickoff_first is True and self._grid_state.period() == 1) or \
                (self.kickoff_first is False and self._grid_state.period() == 2):

            # TODO: [ACT-02] Phase of play account for tactics
            self._team_phase = self.PHASE_BUILDPLAY
            self._set_pieces = self.SP_KICKOFF
        else:
            self._team_phase = self.PHASE_DEFENSIVE
            self._set_pieces = self.SP_NONE

    def filters(self):
        return {
            'Team': {
                'PhaseOfPlay': self._team_phase,
                'SetPieces': self._set_pieces,
            }
        }

    def as_dict(self):
        data = {
            'team_key': self.key(),
            'team_phase': self._team_phase,
            'set_pieces': self._set_pieces,
            'kickoff_first': self.kickoff_first,
            'field_players': [],
        }

        for player in self.field_players:
            data['field_players'].append(player.as_dict())

        return data

    def from_dict(self, data):
        self._team_key = data['team_key']
        self._team_phase = data['team_phase']
        self._set_pieces = data['set_pieces']
        self.kickoff_first = data['kickoff_first']

        for fp in self.field_players:
            playerdata = [pd for pd in data['field_players'] if pd['npc'] == fp.id()]
            fp.from_dict(playerdata[0])

    def players(self):
        return self.field_players

    def debug_getplayercoords(self):
        return [player.current_position for player in self.field_players]


class FieldPlayer:
    # TODO: [ACT-03] Field player roles should be defined in db
    # rather than constants
    ROLE_CAPTAIN = 'captain'
    ROLE_FREE_KICKS = 'field_free_kicks'
    ROLE_PLAYMAKER = 'playmaker'
    ROLE_STRIKER = 'striker'

    all_actions = None

    def __init__(self):
        self.npc = None
        self.attributes = None

        # How the player is initially placed in its zone
        # (the modifiers value +/-)
        self.field_position = None
        # The zone where the player initially starts
        self.field_zone = None
        # Coordinates in the grid where the player is currently placed
        self.current_position = None

        self.team = None
        self.roles = []

        # TODO: [ACT-04] Multiple players can have ball action
        # based on relative distance to
        # the ball of each, when the ball is not
        # in the same cell as any of the players.
        # in this case the action may be performed by
        # the one with best SPEED/INITIATIVE/CONCENTRATION
        self.has_ball_action = False

    def as_dict(self):
        data = {
            'npc': self.npc.pk,
            'pos': self.current_position,
        }
        if len(self.roles) > 0:
            data['roles'] = self.roles

        return data

    def from_dict(self, data):
        self.current_position = tuple(data['pos'])
        if 'roles' in data:
            self.roles = data['roles']

    def init_start_position(self, zone_center, grid):
        from random import randint
        if self.ROLE_FREE_KICKS in self.roles and self.team.kickoff_first:
            # TODO: [ACT-05] Kickoff role should be given by
            # the player based on some logic, not defined by a human
            kickoff_zones = grid.get_kickoff_cell_coords(self.team.key())
            self.current_position = kickoff_zones[0]
            grid.place_player(self)
            # TODO: [ACT-06] 1st tick -> the ball will
            # be passed to the play maker
            grid.give_ball_to(self)
        elif self.ROLE_PLAYMAKER in self.roles and self.team.kickoff_first:
            kickoff_zones = grid.get_kickoff_cell_coords(self.team.key())
            self.current_position = kickoff_zones[1]
            grid.place_player(self)
        else:
            # TODO: [ACT-07] Special placement for all players
            # relative to the center at kickoff
            # TODO: [ACT-08] Get goalkeeper zone and place him
            # TODO: [ACT-09] Randomization limits below are
            # calculated on discipline
            random_diff_x = randint(0, 2)
            random_diff_y = randint(0, 2)
            self.current_position = (
                zone_center[0] + random_diff_x,
                zone_center[1] + random_diff_y
            )
            grid.place_player(self)

    def get_possible_actions(self, filters=None):
        filters = {} if filters is None else filters

        # TODO: [ACT-10] Initially received filters are driven from grid state
        # TODO: [ACT-11] Take team state into account
        # unless already implemented (check)
        filters.update(self.team.filters())
        filters.update({
            'Player': {
                'HasBall': self.has_ball_action
            }
        })

        filtered_actions = self.get_filtered_actions(filters)
        return filtered_actions

    def __str__(self):
        from dream.core.models import Npc
        if type(self.npc) == Npc:
            return ("%s [%s]" % (self.npc, self.team.key())).upper()
        else:
            raise InitError(_('Uninitialized player'))

    def id(self):
        return self.npc.pk

    def init_actions(self):
        # TODO: [ACT-12] Instantiate the action class
        # from the player action with row data
        # Instantiate conditional class and other
        # required classes and compose into action class
        from dream.engine.soccer.models import PlayerAction
        # Filter only allowed actions (fail safe)
        return PlayerAction.objects.filter(enabled=True)

    def get_filtered_actions(self, filters):
        from dream.engine.soccer.match.action import ActionContext
        if FieldPlayer.all_actions is None:
            FieldPlayer.all_actions = self.init_actions()

        context = ActionContext(filters)
        allowed_actions = []

        for action in FieldPlayer.all_actions:
            if context.can_perform_action(action):
                allowed_actions.append(action)

        return allowed_actions

    def decide_action(self, actions):
        """
        The choice of action is made based on player
        (intelligence/reflexes/style of play/etc)
        and random (inspiration). The lower the player
        intelligence/reflexes, the higher the random
        Also if the player is "unpredictable" it will be a higher random
        """
        # TODO Implement as discussed
        from random import choice as random_pick
        return random_pick(actions)

    def perform_action(self, player_action, board):
        from dream.engine.soccer.models import PlayerAction
        if type(player_action) is not PlayerAction:
            raise LoopError(_('Invalid player action'))

        # Import the right class

        print("Performing action...")

        from dream.engine.soccer.match.action import ActionFactory

        factory = ActionFactory.get()
        action_cls = factory.create_action(player_action.name)
        action_inst = action_cls()

        print(action_inst)
        action_inst.perform(player=self, board=board)

        # action_inst.set_player(self)
        # action_inst.set_board(board)
        # action_inst.perform()
        # TODO ^^^
