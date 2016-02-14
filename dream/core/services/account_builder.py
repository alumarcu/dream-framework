class AccountBuilder:
    def build_user(self, data):
        """
        Creates a new user using the model provided by Django framework
        :param data: Should be valid and contain username, email and password as keys
        :return: User
        """
        from django.contrib.auth.models import User
        user = User.objects.create_user(
            data['username'],
            email=data['email'],
            password=data['password']
        )
        return user

    def build_manager(self, user, data):
        """
        Creates the manager identity of a given user
        :param User user: The user for which to create the manager id
        :param data: Additional data to use on initialization
        :return: Manager
        """
        from dream.core.models import Manager
        manager = Manager(user=user, name=data['manager_name'])
        return manager

    def build_club(self, manager, country, data):
        """
        Creates the club from data assumed valid
        :param manager: A Manager instance
        :param country: A Country instance
        :param data: Additional data
        :return: Club
        """
        from dream.core.models import Club
        club = Club(manager=manager, country=country, name=data['club_name'])
        return club

    def build_team(self, club, league):
        from dream.core.models import Team
        team = Team(
            name=club.name,
            club=club,
            gender=league.gender
        )
        return team

    def find_team_division(self, team, league):
        """
        Finds a suitable division for a given team in a league.
        :param team:
        :param league:
        :return:
        """
        from dream.core.models import Division, TeamDivision
        # [TODO][SER-05] Naive implementation that needs to be developed
        division = Division.objects.order_by('level').get(league=league)
        # Does the division have empty seats?
        # What if there are no empty seats in any division?
        # - The user should be placed on a waiting queue and admins notified
        team_division = TeamDivision(team=team, division=division)
        return team_division

    def build_npcs(self, team, club):
        """
        Creates a base set of NPCs for a newly created team
        :param Team team:
        :param Country country:
        :return: []
        """
        from os.path import join
        from random import randint
        from linecache import getline, clearcache
        from dream.settings import BASE_DIR
        from dream.tools import line_count
        from dream.core.models import Npc

        country_code = club.country.country_code
        base_gender = team.gender  # Base gender, non-player NPCs can have random genders

        PLAYERS_PER_TEAM = 18  # [TODO] This should be read from settings of the Sport object

        rootpath = join(BASE_DIR, 'docs', 'names')

        # [TODO][SER-09] Names of NPCs should be read from a db table instead of files
        # Furthermore, a db function to generate a random name would be useful
        file_firstnames = join(rootpath, '%s_%s_fn.txt' % (country_code, base_gender))
        file_lastnames = join(rootpath, '%s_u_ln.txt' % country_code)

        count_firstnames = line_count(file_firstnames)
        count_lastnames = line_count(file_lastnames)

        npcs = []
        for i in range(PLAYERS_PER_TEAM):
            first_name = getline(file_firstnames, randint(1, count_firstnames)).replace("\n", '')
            last_name = getline(file_lastnames, randint(1, count_lastnames)).replace("\n", '')

            npcs.append(Npc(
                club=club,
                team=team,
                first_name=first_name,
                last_name=last_name,
                age=randint(17, 31),  # [TODO] Read this from Sport configuration instead
                gender=team.gender,
            ))

        clearcache()
        return npcs
