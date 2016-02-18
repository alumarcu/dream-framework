from django.views.generic import View
from django.shortcuts import render


class TeamCreatorView(View):

    TEMPLATE_PATH = 'dev/team_creator.html'

    def get(self, request):
        context = {}
        return render(request, self.TEMPLATE_PATH, context)

    def post(self, request):
        pass
