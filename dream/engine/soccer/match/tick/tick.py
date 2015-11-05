class Tick:
    def perform(self):
        pass

    def create_move_queue(self):
        # Returns a list of 22 players and the
        # order in which they should be moved
        pass

    def animate_player(self, player):
        # Moves a FieldPlayer
        pass

    """
    === 1) Get players order of movement based on a base logic
    (i.e. player with ball is first, others are random)
    === 2) Move each player uniformly, considering grid_state changes
    and effects of each player movement on those that follow

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
    """
