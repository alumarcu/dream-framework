from json import loads as json_decode, dumps as json_encode
from dream.engine.soccer.exceptions import SimulationError
from dream.engine.soccer.match.board import Board
from dream.engine.soccer.tools import engine_params
from dream.tools.tools import toss_coin


class SimulationService:
    def fetch_tactics(self, match):
        from dream.core.models import MatchTeam
        match_teams = MatchTeam.objects.filter(match=match)
        tactics = {}
        for mt in match_teams:
            key = mt.role
            decoded_tactics = self.decode_tactics(mt.tactics)
            if self.validate_tactics(decoded_tactics):
                tactics[key] = decoded_tactics
        return tactics

    def decode_tactics(self, tactics_json):
        try:
            decoded_tactics = json_decode(tactics_json)
        except Exception as e:
            raise SimulationError('Could not decode tactics!')
        return decoded_tactics

    def validate_tactics(self, decoded_tactics):
        return True

    def create_board(self):
        board = Board()
        board.initialize()
        return board

    def place_teams_on_board(self, board, tactics):
        # Decide the team that gets to kick off
        kickoff_team = toss_coin(board.team_keys())

        for team_key in board.team_keys():
            team = board.create_field_team(team_key)
            team.field_players = self.create_field_players(team, tactics)
            team.kickoff_first = True if team.key() == kickoff_team else False

            for player in team.field_players:
                board.place_player_on_field(player)

    def create_field_players(self, team, tactics):
        from dream.core.models import Npc, NpcAttribute
        from dream.engine.soccer.match.actors import FieldPlayer

        players = tactics[team.key()]['players']
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

        log = MatchLog(match=match)
        log.sim_minutes_passed = board.grid_state().game_minute
        log.sim_last_tick_id = board.grid_state().tick_id
        log.sim_ticks_per_minute = engine_params(key='match_ticks_per_minute').value
        log.last_saved_state = state_json
        log.journal = journal

        return log

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
