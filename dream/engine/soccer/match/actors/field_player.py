from django.utils.translation import ugettext_lazy as _
from dream.engine.soccer.exceptions import InitError, LoopError


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
        from dream.engine.soccer.match.action import ActionFactory

        board.log('%s is brewing something.' % self.npc)

        factory = ActionFactory.get()
        action_cls = factory.create_action(player_action.name)
        action_inst = action_cls()

        action_inst.perform(player=self, board=board)

        # action_inst.set_player(self)
        # action_inst.set_board(board)
        # action_inst.perform()
        # TODO ^^^
