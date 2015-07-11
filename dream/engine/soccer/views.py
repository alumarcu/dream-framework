from django.views.generic import View
from django.shortcuts import render
from dream.engine.soccer.match.simulation import DebugMatch
from django.http import JsonResponse, HttpResponse
from json import dumps as json_encode


class DebugView(View):

    TEAMPLATE_PATH = 'debug/match.html'

    def get(self, request, match_id):
        print('[GET]Match ID is:', match_id)
        match_id = int(match_id)   # Taken from URL

        sim = DebugMatch()
        sim.add_match(match_id)
        sim.initialize()

        context = {
            'message': "test message from view",
            'board_state': json_encode(sim.debug_data())
        }

        return render(request, self.TEAMPLATE_PATH, context)

    def post(self, request, match_id):
        print('[POST]Match ID is:', match_id)
        match_id = int(match_id)   # Taken from URL

        # TODO: [DBG-01] Process AJAX requests here
        # and return updated debug JSON
        print(request.POST['MESSAGE'])   # This will print to command line ok

        sim = DebugMatch()
        sim.add_match(match_id)
        sim.initialize()
        sim.loop()

        context = {
            'board_state': sim.debug_data()
        }

        # Next it will complain that no response was sent
        # TODO keep up the good work!, make a new tick and send the new board state
        #return JsonResponse({'foo': 'bar'})

        # TODO Client-side parsing of player coordinates
        return JsonResponse(context)
