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
        from dream.engine.soccer.models import ActionRequirement

        current_val = None
        if req_key in self._current:
            current_val = self._current[req_key]

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
