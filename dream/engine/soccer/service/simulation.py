from json import loads as json_decode, dumps as json_encode
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _

from dream.engine.soccer.exceptions import InitError, SimulationError
from dream.engine.soccer.match.board import Board
from dream.engine.soccer.tools import engine_params
from dream.tools import Logger, toss_coin


class SimulationService:
    def __init__(self, match):
        self.logger = Logger(__name__, Logger.default_message)
        self.match = match
        self.tactics = self._fetch_tactics(self.match)

    def validate_tactics(self, decoded_tactics):
        return True

    def resume_board(self, tick_id):
        """
        Resumes board at given tick
        :param tick_id:
        :type tick_id:
        :return:
        :rtype:
        """
        from dream.engine.soccer.match.board import Grid
        self.logger.log('LOAD EXISTING BOARD AT TICK %s' % tick_id)

        match_log = self.go_to_tick(self.match, tick_id)
        """:type : dream.core.models.MatchLog"""

        match_state = json_decode(match_log.state)
        board_data = match_state['board']
        teams_data = board_data['teams']
        grid_data = board_data['grid']

        # TODO: from_dict no longer required
        board = (Board(template=self.match.board_template)).from_dict(board_data)

        for team_key in teams_data:
            team = board.create_field_team(team_key)
            team.field_players = self.create_field_players(team)
            team.from_dict(teams_data[team_key])
            board.teams[team_key] = team

        fp_cache = {}  # player IDs => FieldPlayer
        for team in board.teams.values():
            for fp in team.players():
                fp.team = team
                fp_cache[fp.id()] = fp

        grid = Grid()
        grid.initialize(template=board.template)

        grid.state.tick_id = match_log.tick
        grid.state.game_minute = match_log.minute
        grid.state.player_with_ball = match_log.player_with_ball
        grid.state.action_status(match_log.action_status)

        board.grid = grid.from_dict(grid_data, fp_cache)

        return board, match_log, match_state

    def create_board(self):
        self.logger.log('CREATE NEW BOARD')

        board = Board(template=self.match.board_template)
        board.initialize()
        # TODO: Logic for board initialization on second half.

        self.place_teams_on_board(board)

        return board

    def place_teams_on_board(self, board):
        # Decide the team that gets to kick off
        kickoff_team = toss_coin(board.team_keys())

        for team_key in board.team_keys():
            team = board.create_field_team(team_key)
            team.field_players = self.create_field_players(team)
            team.kickoff_first = True if team.key() == kickoff_team else False

            for player in team.field_players:
                board.place_player_on_field(player)

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

    def create_board_state_log(self, board, match, journal):
        from dream.core.models import MatchLog

        state = {'board': board.as_dict()}
        state_json = json_encode(state, separators=(',', ':'))

        ml = MatchLog(match=match)
        ml.minute = board.grid_state().game_minute
        ml.tick = board.grid_state().tick_id
        ml.state = state_json
        ml.journal = journal

        return ml

    def create_player_action_ordering(self, players_list, kickoff_team):
        """
        Returns the order in which players execute actions during a tick;
        this is not calculated per team, but for all players on the field
        :return:    The list of players in the calculated order
        """
        # TODO: [SIM-06] Better movement order based on INITIATIVE, DISTANCE TO BALL, TEAM, ETC
        from random import shuffle
        shuffle(players_list)
        return players_list

    def go_to_tick(self, match, tick_id):
        from dream.core.models import MatchLog

        filters = {'match': match}

        try:
            if tick_id != -1:
                filters['tick'] = tick_id
                match_log = MatchLog.objects.get(**filters)
            else:
                match_log = MatchLog.objects\
                    .filter(**filters)\
                    .latest('tick')

        except ObjectDoesNotExist:
            raise InitError(_('Tick with id: {} does not exist for match_id: {}'
                            .format(tick_id, match.pk)))

        return match_log

    def _fetch_tactics(self, match):
        from dream.core.models import MatchTeam

        match_teams = MatchTeam.objects.filter(match=match)
        tactics = {}
        for mt in match_teams:
            key = mt.role
            decoded_tactics = self._decode_tactics(mt.tactics)
            if self.validate_tactics(decoded_tactics):
                tactics[key] = decoded_tactics
        return tactics

    def _decode_tactics(self, tactics_json):
        try:
            decoded_tactics = json_decode(tactics_json)
        except Exception as e:
            raise SimulationError('Could not decode tactics!')
        return decoded_tactics
