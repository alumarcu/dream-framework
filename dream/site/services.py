from django.db import transaction
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from dream.tools import line_count
from dream.core.models import Club, Manager, Team, Npc, Country, Division, League, TeamDivision


class SignupService:
    # TODO: [SER-01] Initial players in team: database parameter should be created
    INITIAL_PLAYERS_IN_TEAM = 18

    def __init__(self):
        self.user = None
        self.manager = None
        self.club = None
        self.team = None

        self._user_data = None

    @transaction.atomic()
    def create_user(self, user_data):
        if not self.is_valid_user_data():
            return

        self._user_data = user_data

        self.user = self._create_user()
        self.user.save()

        self.manager = self._create_manager()
        self.manager.save()

        self.club = self._create_club()
        self.club.save()

        # TODO: [SER-04] Register the team in a league chosen by user; if more than 1 are available
        picked_league = League.objects.get(country=self.club.country)

        self.team = self._create_team(picked_league)
        self.team.save()

        teamdiv = self._assign_to_division(picked_league)
        teamdiv.save()

        npcs = self._create_npcs()
        for npc in npcs:
            npc.save()

    def is_valid_user_data(self):
        # TODO: [SER-02] Validation of keys for user data
        return True

    def _create_manager(self):
        return Manager(
            user=self.user,
            name=self._user_data['managername']
        )

    def _create_user(self):
        return User.objects.create_user(
            self._user_data['username'],
            email=self._user_data['email'],
            password=self._user_data['passwda']
        )

    def _create_team(self, league):
        return Team(
            # TODO: [SER-06] User should be able to decide if the
            # name of the team is same as club's
            name=self.club.name,
            club=self.club,
            # TODO: [SER-07] TBD - choice of gender before choice or league or vice versa
            gender=league.gender
        )

    def _assign_to_division(self, league):
        # TODO: [SER-05] Logic for matching team to division
        assigned_division = Division.objects.order_by('level').get(league=league)
        return TeamDivision(
            team=self.team,
            division=assigned_division
        )

    def _create_club(self):
        country = Country.objects.get(pk=self._user_data['country'])

        if not isinstance(country, Country):
            # TODO: [SER-03] Create relevant exceptions for Service and Signup
            # process, or just generic site errors
            print(_('invalid country: %s' % self._user_data['country']))
            exit()

        return Club(
            manager=self.manager,
            country=country,
            name=self._user_data['clubname']
        )

    def _create_npcs(self):
        from os.path import join
        from random import randint
        from linecache import getline, clearcache
        from dream.settings import BASE_DIR

        ccode = self.club.country.country_code
        cgender = self.team.gender

        rootpath = join(BASE_DIR, 'docs', 'names')

        # TODO: [SER-09] Names of NPCs should be read from a database table rather than flat files
        # Furthermore, a database function to automatically
        # generate a random name would be useful here
        file_firstnames = join(rootpath, '%s_%s_fn.txt' % (ccode, cgender))
        file_lastnames = join(rootpath, '%s_u_ln.txt' % ccode)

        count_firstnames = line_count(file_firstnames)
        count_lastnames = line_count(file_lastnames)

        npcs = []
        for i in range(self.INITIAL_PLAYERS_IN_TEAM):
            first_name = getline(file_firstnames, randint(1, count_firstnames)).replace("\n", '')
            last_name = getline(file_lastnames, randint(1, count_lastnames)).replace("\n", '')

            npcs.append(Npc(
                club=self.club,
                team=self.team,
                first_name=first_name,
                last_name=last_name,
                age=randint(17, 31),
                gender=self.team.gender,
            ))

        clearcache()
        return npcs
