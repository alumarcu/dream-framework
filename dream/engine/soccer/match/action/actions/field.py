from dream.engine.soccer.match.action.action import Action


class FieldAction(Action):
    def perform(self):
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
