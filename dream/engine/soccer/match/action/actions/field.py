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
