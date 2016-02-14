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

    def __init__(self, match_team):
        """
        :type match_team: dream.core.models.MatchTeam
        :return:
        """
        self.team_key = match_team.role
        self.match_team = match_team

        self.kickoff_first = None
        self.field_players = []

        self.grid_state = None
        self.action_phase = None
        self.resume_phase = None

    def key(self):
        return self.team_key

    def initialize(self, grid_state):
        self.grid_state = grid_state
        self.init_phase()

    def init_phase(self):
        # TODO: [ACT-01] Phase of play should change based on
        # which third is the ball in
        # and to whom it belongs as well as individual team tactics
        if (self.kickoff_first is True and self.grid_state.period() == 1) or \
                (self.kickoff_first is False and self.grid_state.period() == 2):

            # TODO: [ACT-02] Phase of play account for tactics
            self.action_phase = self.PHASE_BUILDPLAY
            self.resume_phase = self.SP_KICKOFF
        else:
            self.action_phase = self.PHASE_DEFENSIVE
            self.resume_phase = self.SP_NONE

    def filters(self):
        return {
            'Team': {
                'PhaseOfPlay': self.action_phase,
                'SetPieces': self.resume_phase,
            }
        }

    def resume(self, match_team_log):
        """
        :type match_team_log: dream.engine.soccer.models.MatchTeamLog
        :return: self
        """
        from json import loads as json_decode

        self.team_key = match_team_log.match_team.role
        self.action_phase = match_team_log.action_phase
        self.resume_phase = match_team_log.resume_phase
        self.kickoff_first = match_team_log.kick_off

        player_loc_data = json_decode(match_team_log.players)
        for fp in self.field_players:
            player_data = [pd for pd in player_loc_data if pd['npc'] == fp.id()]
            fp.resume(player_data[0])

        return self

    def players(self):
        return self.field_players

    def match_info_get_player_coordinates(self):
        return [player.current_position for player in self.field_players]

    def __str__(self):
        return '<FieldTeam: "%s">' % self.team_key
