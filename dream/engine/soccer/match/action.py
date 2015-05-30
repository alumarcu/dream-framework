from django.utils.translation import ugettext_lazy as _
from dream.engine.soccer.exceptions import LoopError


class ActionFactory:

    def __init__(self):
        self._map = {
            'Pass': PassAction,
            'Indirect_Kick_Pass': IndirectKickPassAction,
            'Move_Defensive': DefensivePositionAction,
            'Move_Offensive': OffensivePositionAction
        }

    @staticmethod
    def get():
        if not hasattr(ActionFactory, 'instance'):
            ActionFactory.instance = ActionFactory()
        return ActionFactory.instance

    def create_action(self, class_name):
        if class_name not in self._map:
            LoopError(_('Invalid class name %s' % class_name))
        return self._map[class_name]


class ActionContext:

    _current = None

    def __init__(self, filter_dict):

        # {'Player': {'HasBall': True}, 'Game': {'ActionStatus':
        # 'play_interrupted', 'TickId': 1}, 'Team': {'PhaseOfPlay': 'phase_
        # buildplay', 'SetPieces': 'setpieces_kickoff'}}
        self._current = {}

        for section, requires in filter_dict.items():
            for key, value in requires.items():
                self._current[section + '.' + key] = value

        # print(self._current)

    def can_perform_action(self, player_action):
        """
        Match against the requirements of an action
        """
        from dream.engine.soccer.models import ActionRequirement
        requirements = ActionRequirement.objects.filter(action=player_action)
        # Stack requirements with can_be
        print(">>>>>>>>>>", player_action.name)

        action_context = {}

        for action_requirement in requirements:
            action_context.update(
                ActionContext.parse_action_requirement(action_requirement))

        # Now check each requirement as it's being iterated over
        for req_key, req_data in action_context.items():
            if not self.meets_requirement(req_key, req_data):
                return False

        return True

    @staticmethod
    def parse_action_requirement(ar):
        """
        Parses an action-requirement mapping based on the type of requirement
        """
        from dream.engine.soccer.models import Requirement

        requirement_type = ar.requirement.type
        required_values = None

        if requirement_type == Requirement.TYPE_BOOL:
            required_values = True \
                if ar.value == Requirement.VAL_BOOL_TRUE else False
        elif requirement_type == Requirement.TYPE_INT:
            required_values = int(ar.value)
        elif requirement_type == Requirement.TYPE_ENUM:
            from json import loads as json_decode

            # IDs of values that are required
            value_ids = json_decode(ar.value)
            # Getting the actual values from IDs
            enum_values = ar.requirement.enum_values(value_ids)
            required_values = [ev.value for ev in enum_values]

        req_key = ar.requirement.name
        req_data = {
            'condition': ar.condition,
            'required_values': required_values,
        }

        return {req_key: req_data}

    def meets_requirement(self, req_key, req_data):
        from dream.engine.soccer.models import Requirement, ActionRequirement
        # if type(action_requirement) != PlayerActionRequirement:
        #     exit("Bad player requirement")

        current_val = None
        if req_key in self._current:
            current_val = self._current[req_key]
        print("vvvvvvvvvvvvvvvvv")
        print(req_key)
        print(current_val)
        print(req_data)
        print("^^^^^^^^^^^^^^^^^")

        req_value = req_data['required_values']
        if req_data['condition'] == ActionRequirement.CONDITION_IS:
            if type(req_value) == list and len(req_value) > 0:
                req_value = req_value[0]
            if current_val != req_value:
                return False
        if req_data['condition'] == ActionRequirement.CONDITION_CAN_BE:
            if current_val not in req_value:
                return False
        if req_data['condition'] == ActionRequirement.CONDITION_ABOVE:
            if current_val <= req_value:
                return False
        if req_data['condition'] == \
                ActionRequirement.CONDITION_ABOVE_OR_EQUAL:
            if current_val < req_value:
                return False
        if req_data['condition'] == ActionRequirement.CONDITION_BELOW:
            if current_val >= req_value:
                return False
        if req_data['condition'] == \
                ActionRequirement.CONDITION_BELOW_OR_EQUAL:
            if current_val > req_value:
                return False

        return True


class FieldAction:
    # TODO: Create base abstract methods!!
    # player = None
    # board = None

    def perform(self, player, board):
        # TODO: Check instance types
        pass

    def check_dependencies(self):
        # TODO check_dependencies
        """
        An action may depend on the existence of certain player
        attributes in database, or other db-side values. Use this
        method to make sure the action can apply and is compatible with
        what's defined on database
        """
        return True


class BallAction(FieldAction):

    def move_ball(self, source_cell, target_cell):
        # Remove ball from player in the current grid cell
        source_cell.has_ball = None
        source_cell.player_with_ball.has_ball_action = False
        source_cell.player_with_ball = None

        target_cell.has_ball = True

        ball_winner = self.get_ball_winner(target_cell.players)
        if ball_winner is not False:
            target_cell.give_ball_to(ball_winner)

    def get_ball_winner(self, players_on_cell):
        if len(players_on_cell) == 0:
            return False
        # TODO --> Competition for ball between two players
        # in same cell, or just random
        return players_on_cell[0]


class PassAction(BallAction):
    pass


class IndirectKickPassAction(PassAction):

    def perform(self, player, board):
        print("-------------------------------")
        print(player.current_position)
        print(player.field_zone)

        grid = board.grid
        current_grid_cell = grid.get_cell(player.current_position)
        next_grid_cell = None

        if player.ROLE_FREE_KICKS in player.roles and \
                player.team.kickoff_first:
            # TODO: Negate and quit OR validate

            print("The player kicks off the ball")
            kickoff_zones = grid.get_kickoff_cell_coords(player.team.key())
            # Coords of the next grid cell
            next_position = kickoff_zones[1]
            next_grid_cell = grid.get_cell(next_position)

            self.move_ball(current_grid_cell, next_grid_cell)


class MoveAction(FieldAction):
    pass


class OffensivePositionAction(MoveAction):

    def perform(self, player, board):
        print("-------------------------------")
        print(player.current_position)
        print(player.field_zone)

        grid = board.grid
        curr_coords = player.current_position
        coords = (curr_coords[0], curr_coords[1] + 15)   # Advance on y-pos

        print("%s moves to %s" % (player, coords))
        grid.move_player(player, coords)


class DefensivePositionAction(MoveAction):
    pass
