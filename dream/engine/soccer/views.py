from django.views.generic import View
from django.shortcuts import render
from dream.engine.soccer.match.simulation import DebugMatch


class DebugView(View):

    TEAMPLATE_PATH = 'debug/match.html'

    def get(self, request, match_id):
        print('Match ID is:', match_id)
        match_id = int(match_id)   # Taken from URL

        sim = DebugMatch()
        sim.add_match(match_id)
        sim.initialize()

        context = {
            'message': "FOOO",
            'board_state': sim.debug_data()
        }

        return render(request, self.TEAMPLATE_PATH, context)

    def post(self, request):
        # TODO: [DBG-01] Process AJAX requests here
        # and return updated debug JSON
        pass
