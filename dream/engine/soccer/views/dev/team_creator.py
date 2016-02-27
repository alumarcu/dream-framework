from django.views.generic import View
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count


class TeamCreatorView(View):

    TEMPLATE_PATH = 'dev/team_creator.html'

    def get(self, request):
        """
        :type request: django.http.HttpRequest
        :return:
        """
        context = {}
        return render(request, self.TEMPLATE_PATH, context)

    def post(self, request):
        query = request.POST
        response = {}

        if request.is_ajax:
            if 'clubs-table' in query:
                response.update(self.get_clubs_table(query))

        return JsonResponse(response)

    def get_clubs_table(self, query):
        from dream.core.models import Team

        columns = [
            'club__pk',
            'club__name',
            'club__manager__name',
            'club__country__name',
            'club__created'
        ]

        # TODO: Take into account pagination and ordering (from query)
        clubs = Team.objects \
            .values(*columns) \
            .annotate(team_count=Count('pk'))

        table_data = []

        for club in clubs:
            row = {
                'team_count': club['team_count'],
                'manager_name': club['club__manager__name'],
                'club_name': club['club__name'],
                'country': club['club__country__name'],
                'created': club['club__created'].strftime('%d-%m-%Y %H:%M:%S'),
                'actions': club['club__pk']
            }

            table_data.append(row)

        return {
            'data': table_data,
            'draw': query['draw'],
            'recordsTotal': len(clubs),
            'recordsFiltered': len(clubs)
        }
