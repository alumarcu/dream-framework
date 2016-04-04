from django.views.generic import View
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count
from json import loads as json_decode


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

        if 'clubs-table' in query:
            response.update(self.get_clubs_table(query))
        if 'new-club' in query:
            response.update(self.create_new_club(query))

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

    def create_new_club(self, query):
        from django.utils.html import escape
        from django.utils.text import slugify
        from dream.site.services import SignupService

        form_data = json_decode(query['new-club'])

        data = {}
        data['manager_name'] = escape(form_data['manager-name'])
        data['username'] = slugify(data['manager_name']).replace('-', '_')
        data['email'] = data['username'].replace('-', '') + '@dream11.io'
        data['club_name'] = escape(form_data['club-name'])

        data['country'] = 1  # Assumed to be "intl"
        data['password'] = 'dev'

        response = {'is_error': False}

        try:
            service = SignupService()
            service.create_account(data)
        except Exception as e:
            response['is_error'] = True
            response['message'] = str(e)

        return response
