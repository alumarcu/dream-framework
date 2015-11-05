from django.views.generic import View
from django.shortcuts import render
from dream.engine.soccer.match.simulation import DebugMatch
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
        response = {}
        response['setup-data'] = {
            'grid_width': engine_params(key='grid_width').value,
            'grid_length': engine_params(key='grid_length').value,
        }
        return response

    def get_match_info(self, query, match_id):
        response = {}

        if 'get-ticks' in query:
            response.update(self.get_ticks(query, match_id))
        if 'get-board' in query:
            response.update(self.get_board(query, match_id))
        if 'new-tick' in query:
            response.update(self.new_tick(query, match_id))
        if 'delete-ticks' in query:
            response.update(self.delete_ticks(query, match_id))

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

        sim = DebugMatch()
        sim.add_match(match_id)
        sim.initialize()

        response['board-state'] = json_encode(sim.debug_data())
        return response

    def new_tick(self, query, match_id):
        response = {}

        sim = DebugMatch()
        sim.add_match(match_id)
        sim.initialize()
        # TODO: Move shared functionality somewhere else;
        # a simulation method should do specifically what is requested -
        # create a new tick but not start a loop (called in loop though)
        sim.loop()

        response['board_state'] = json_encode(sim.debug_data())
        return response

    def delete_ticks(self, query, match_id):
        response = {}
        return response
