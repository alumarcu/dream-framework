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
            'message': "test message from view",
            'board_state': sim.debug_data()
        }

        return render(request, self.TEAMPLATE_PATH, context)

    def post(self, request, match_id):
        # TODO: [DBG-01] Process AJAX requests here
        # and return updated debug JSON
        print(request.POST['MESSAGE'])   # This will print to command line ok

        # Next it will complain that no response was sent
        # TODO keep up the good work!, make a new tick and send the new board state
        pass
