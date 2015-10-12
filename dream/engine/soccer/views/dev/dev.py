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
        context = {}

        # **** Fetches matches and teams from the dev league ****
        from dream.core.models import MatchTeam
        match_teams = MatchTeam.objects.\
            filter(match__division__league=1).\
            values('match__id', 'team__name', 'role')

        matches = {}
        for team in match_teams:
            if team['match__id'] not in matches:
                matches[team['match__id']] = {}
            matches[team['match__id']][team['role']] = team['team__name']

        context['matches'] = matches
        # **** End fetching matches ****

        # **** AJAX Calls ****
        query = request.GET

        if 'id' in query:
            if 'ticks' in query:
                match_id = int(query['id'])
                # Match exists; return match related data
                context['info'] = 'Data for match id %d' % match_id
                context['data'] = []

                match_log_rows = MatchLog.objects.filter(match__pk=match_id)
                if len(match_log_rows) > 0:
                    context_logs = []
                    for log in match_log_rows:
                        new_log = {
                            'tick_id': log.pk,
                            'sim_minutes_passed': log.sim_minutes_passed,
                            'sim_last_tick_id': log.sim_last_tick_id,
                            'last_modified': log.last_modified,
                            'journal': log.journal
                        }
                        context_logs.append(new_log)
                    context['data'] = context_logs

                return JsonResponse(context)

            if 'board' in query:
                match_id = int(query['id'])

                sim = DebugMatch()
                sim.add_match(match_id)
                sim.initialize()

                context['board_state'] = json_encode(sim.debug_data())
                return JsonResponse(context)

            if 'next_tick' in query:
                match_id = int(query['id'])

                sim = DebugMatch()
                sim.add_match(match_id)
                sim.initialize()
                sim.loop()

                context['board_state'] = json_encode(sim.debug_data())
                return JsonResponse(context)

        if 'setup' in query:
            context['setup'] = {
                # TODO: Use defensive programming -> validate that engine params exist
                'grid_width': engine_params(key='grid_width').value,
                'grid_length': engine_params(key='grid_length').value,
            }

            return JsonResponse(context)
        # **** END AJAX Calls ****

        return render(request, self.TEAMPLATE_PATH, context)

    # def post(self, request, match_id):
    #     print('[POST]Match ID is:', match_id)
    #     match_id = int(match_id)   # Taken from URL
    #
    #     # TODO: [DBG-01] Process AJAX requests here
    #     # and return updated debug JSON
    #     print(request.POST['MESSAGE'])   # This will print to command line ok
    #
    #     sim = DebugMatch()
    #     sim.add_match(match_id)
    #     sim.initialize()
    #     sim.loop()
    #
    #     context = {
    #         'board_state': sim.debug_data()
    #     }
    #
    #     # Next it will complain that no response was sent
    #     # TODO keep up the good work!, make a new tick and send the new board state
    #     #return JsonResponse({'foo': 'bar'})
    #
    #     # TODO Client-side parsing of player coordinates
    #     return JsonResponse(context)
