from django.views.generic import View
from django.shortcuts import render
from dream.engine.soccer.match.simulation import ManualMatch
from django.http import JsonResponse
from json import dumps as json_encode
from dream.core.models import MatchLog
from dream.engine.soccer.tools import engine_params


class SimulatorView(View):

    TEAMPLATE_PATH = 'dev/simulator.html'

    def get(self, request):
        context = {
            'matches': self.get_dev_matches()
        }
        return render(request, self.TEAMPLATE_PATH, context)

    def post(self, request):
        query = request.POST
        response = {}

        if 'setup' in query:
            response.update(self.get_board_setup(query))
        if 'match-id' in query:
            response.update(self.get_match_info(query, int(query['match-id'])))

        return JsonResponse(response)

    def get_dev_matches(self):
        from dream.core.models import MatchTeam

        match_teams = MatchTeam.objects.\
            filter(match__division__league=1).\
            values('match__id', 'team__name', 'role')

        matches = {}
        for team in match_teams:
            if team['match__id'] not in matches:
                matches[team['match__id']] = {}
            matches[team['match__id']][team['role']] = team['team__name']

        return matches

    def get_board_setup(self, query):
        from dream.core.models import BoardTemplate

        # This is considered to be default
        template_param = engine_params('template')
        """:type : dream.core.models.EngineParam"""

        template_id = template_param.value

        tmpl = BoardTemplate.objects.get(pk=template_id)
        """:type : dream.core.models.BoardTemplate"""

        response = {}
        response['setup-data'] = {
            'grid_width': tmpl.width(),
            'grid_length': tmpl.height(),
        }
        return response

    def get_match_info(self, query, match_id):
        response = {}

        if 'new-tick' in query:
            response.update(self.new_tick(query, match_id))
        if 'delete-ticks' in query:
            response.update(self.delete_ticks(query, match_id))
        # Getters should always be handled last (after delete or create)
        if 'get-ticks' in query:
            response.update(self.get_ticks(query, match_id))
        if 'get-board' in query:
            response.update(self.get_board(query, match_id))

        response.update(self.get_match_stats(query, match_id))

        return response

    def get_ticks(self, query, match_id):
        response = {}
        requested_ticks = int(query['get-ticks'])

        if requested_ticks == -1:
            match_log_rows = MatchLog.objects.filter(match__pk=match_id)
        else:
            match_log_rows = MatchLog\
                .objects\
                .filter(
                    match__pk=match_id,
                    tick__lte=requested_ticks
                )

        if len(match_log_rows) > 0:
            match_logs = []
            for log in match_log_rows:
                new_log = {
                    'tick_id': log.pk,
                    'minute': log.minute,
                    'tick': log.tick,
                    'modified': log.modified
                }
                match_logs.append(new_log)
            response['ticks-list'] = match_logs

        return response

    def get_board(self, query, match_id):
        response = {}

        mm = ManualMatch(match_id)
        mm.initialize(tick_id=-1)

        response['board-state'] = json_encode(mm.match_info())
        return response

    def new_tick(self, query, match_id):
        response = {}

        mm = ManualMatch(match_id)
        mm.initialize(tick_id=-1)
        mm.begin_simulation()
        mm.create_tick()
        # TODO: Move shared functionality somewhere else;
        # a simulation method should do specifically what is requested -
        # create a new tick but not start a loop (called in loop though)

        response['tick-log'] = json_encode(mm.last_tick_info())
        return response

    def delete_ticks(self, query, match_id):
        """
        Deletes everything after a given tick (but not that tick)
        """
        response = {}
        # TODO: These methods may also be moved elsewhere
        delete_after_tick = int(query['delete-ticks'])

        MatchLog\
            .objects\
            .filter(
                match__pk=match_id,
                tick__gt=delete_after_tick
            )\
            .delete()

        # [TBD] Such actions should later be logged?
        return response

    def get_match_stats(self, query, match_id):
        """
        Info provided for any api call with match-id
        :return:    updated response
        :rtype:     dict
        """
        response = {}

        from dream.core.models import MatchTeam

        mts = MatchTeam.objects.filter(match__pk=match_id)
        stats = {}
        for mt in mts:
            if mt.role == 'home':
                stats['home-name'] = mt.team.name
                stats['home-points'] = mt.points
            if mt.role:
                stats['away-name'] = mt.team.name
                stats['away-points'] = mt.points

        response['match-stats'] = stats
        return response
