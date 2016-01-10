from django.utils.translation import ugettext_lazy as _
from dream.engine.soccer.exceptions import SimulationError
from dream.engine.soccer.match.board import Board


class Ticker:
    def __init__(self, board):
        self.board = board
        self.logged = []

    def perform(self):
        if type(self.board) is not Board:
            raise SimulationError(_('Board not initialized in the ticker!'))

        gs = self.board.grid_state()
        gs.tick(new_tick=True)

        move_queue = self.create_move_queue()

        for player in move_queue:
            self.animate_player(player)

    def create_move_queue(self):
        # Returns a list of 22 players and the
        # order in which they should be moved
        players_list = []
        for field_team in self.board.teams.values():
            players_list += field_team.field_players

        move_queue = []
        gs = self.board.grid_state()
        move_queue.append(gs.player_with_ball)
        players_list.remove(gs.player_with_ball)

        # TODO: This should be calculated better based on player skills and match state
        # such as initiative, distance to ball, team, etc.
        import random
        while len(players_list) > 0:
            # for player in players_list:
            player = random.choice(players_list)
            players_list.remove(player)
            move_queue.append(player)

        # We know who is (gs.player_with_ball)
        return move_queue

    def animate_player(self, player):
        self.log('{} has the next action.'.format(player))

        # Move the FieldPlayer
        possible_actions = player.get_possible_actions()
        self.log('Possible actions are: {}'.format(possible_actions))

    def log(self, message):
        self.logged.append(self.board.log(message))

    def get_log(self):
        ret = self.logged
        self.logged = []
        return ret

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
