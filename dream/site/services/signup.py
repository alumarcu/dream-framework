from django.db import transaction

from dream.tools import Logger
from dream.core.services import AccountBuilder
from dream.core.models import Country, League, Npc


class SignupService:
    def __init__(self):
        self.logger = Logger(__name__, Logger.default_message)

    def process(self, payload):
        return payload

    @transaction.atomic()
    def create_account(self, data):
        builder = AccountBuilder()

        user = builder.build_user(data)
        user.save()

        manager = builder.build_manager(user, data)
        manager.save()

        country = Country.objects.get(pk=data['country'])
        club = builder.build_club(manager, country, data)
        club.save()

        # [TODO][SER-04] Register the team in a league chosen by user
        # - since more than one league may be available for a country
        league = League.objects.get(country=country)

        team = builder.build_team(club, league)
        team.save()

        team_division = builder.find_team_division(team, league)
        team_division.save()

        npcs = builder.build_npcs(team, club)
        Npc.objects.bulk_create(npcs)
