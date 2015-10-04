class FieldTeam:
    PHASE_OFFENSIVE = 'phase_offensive'
    PHASE_BUILDPLAY = 'phase_buildplay'
    PHASE_COUNTERATTACK = 'phase_counterattack'
    PHASE_PRESSING = 'phase_pressing'
    PHASE_DEFENSIVE = 'phase_defensive'

    SP_FREEKICK = 'setpieces_freekick'
    SP_CORNER = 'setpieces_corner'
    SP_THROWIN = 'setpieces_throwin'
    SP_GOALKICK = 'setpieces_goalkick'
    SP_KICKOFF = 'setpieces_kickoff'
    SP_INDIRECT_FREEKICK = 'setpieces_indirectfreekick'
    SP_NONE = 'setpieces_none'

    _team_key = None
    _grid_state = None
    _team_phase = None
    _set_pieces = None

    def __init__(self, team_key):
        self._team_key = team_key

        self.kickoff_first = None
        self.field_players = []

    def key(self):
        return self._team_key

    def initialize(self, grid_state):
        self._grid_state = grid_state
        self.init_phase()

    def init_phase(self):
        # TODO: [ACT-01] Phase of play should change based on
        # which third is the ball in
        # and to whom it belongs as well as individual team tactics

        if (self.kickoff_first is True and self._grid_state.period() == 1) or \
                (self.kickoff_first is False and self._grid_state.period() == 2):

            # TODO: [ACT-02] Phase of play account for tactics
            self._team_phase = self.PHASE_BUILDPLAY
            self._set_pieces = self.SP_KICKOFF
        else:
            self._team_phase = self.PHASE_DEFENSIVE
            self._set_pieces = self.SP_NONE

    def filters(self):
        return {
            'Team': {
                'PhaseOfPlay': self._team_phase,
                'SetPieces': self._set_pieces,
            }
        }

    def as_dict(self):
        data = {
            'team_key': self.key(),
            'team_phase': self._team_phase,
            'set_pieces': self._set_pieces,
            'kickoff_first': self.kickoff_first,
            'field_players': [],
        }

        for player in self.field_players:
            data['field_players'].append(player.as_dict())

        return data

    def from_dict(self, data):
        self._team_key = data['team_key']
        self._team_phase = data['team_phase']
        self._set_pieces = data['set_pieces']
        self.kickoff_first = data['kickoff_first']

        for fp in self.field_players:
            playerdata = [pd for pd in data['field_players'] if pd['npc'] == fp.id()]
            fp.from_dict(playerdata[0])

    def players(self):
        return self.field_players

    def debug_getplayercoords(self):
        return [player.current_position for player in self.field_players]
