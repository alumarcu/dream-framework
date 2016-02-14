class GridCell:

    def __init__(self, parent_grid, x_pos, y_pos):
        self.parent_grid = parent_grid
        self.players = []
        self.x_pos = x_pos
        self.y_pos = y_pos

        self.player_with_ball = None
        self.has_ball = None
        self.parent_zone = None  # TODO: A grid cell must know its zone and edge of the zone

    def add_player(self, player):
        self.players.append(player)

    def remove_player(self, player):
        self.players.remove(player)

    def has_players(self):
        return len(self.players) > 0

    def give_ball_to(self, player):
        if player in self.players:
            player.has_ball_action = True
            self.player_with_ball = player
            self.has_ball = True

    def __str__(self):
        if self.player_with_ball is not None:
            return '0'
        if self.has_players():
            return 'o'
        if self.has_ball:
            return '*'  # There's a ball here, but no player controls it
        if self.is_corner_edge() and self.is_oop_edge():
            return '+'
        if self.is_corner_edge():
            return '-'
        if self.is_oop_edge():
            return '|'

        return '.'

    def is_oop_edge(self):
        return self.x_pos == self.parent_grid.width - 1 or self.x_pos == 0

    def is_corner_edge(self):
        return self.y_pos == self.parent_grid.length - 1 or self.y_pos == 0

    def export(self):
        data = {}
        has_something = False

        if self.has_ball is True:
            data['has_ball'] = self.has_ball
            has_something = True
        if self.player_with_ball is not None:
            data['player_with_ball'] = self.player_with_ball.id()
            has_something = True
        if len(self.players) > 0:
            data['players'] = [p.id() for p in self.players]
            has_something = True
        if has_something:
            data['xy'] = [self.x_pos, self.y_pos]

        return data
