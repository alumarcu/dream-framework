from django.db.models import Model, CharField, DateTimeField, ForeignKey, \
    IntegerField, SmallIntegerField, BooleanField, TextField, DecimalField
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from dream.tools import create_reference


GENDER_MALE = 'm'
GENDER_MALE_TEXT = _('Male')
GENDER_FEMALE = 'f'
GENDER_FEMALE_TEXT = _('Female')
GENDER_UNDEFINED = 'u'
GENDER_UNDEFINED_TEXT = _('N/A')

GENDER_CHOICES = (
    (GENDER_MALE, GENDER_MALE_TEXT),
    (GENDER_FEMALE, GENDER_FEMALE_TEXT)
)


class Sport(Model):
    name = CharField(max_length=40)
    # TODO: [MOD-01] Correspondence between NPC roles and the sports they are
    # relevant to.
    # For example, it should be possible for a club to have the same medics
    # used for both the men's soccer team and women's handball. A Sport can
    # have multiple Roles associated (N to N assoc)

    def __str__(self):
        return self.name


class Country(Model):
    name = CharField(_('country name'), max_length=60)
    country_code = CharField(_('country iso code'), max_length=5)

    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = _('countries')


class League(Model):
    """
    Is defined by a country and a sport and contains a collection of divisions
    """
    country = ForeignKey(Country)
    sport = ForeignKey(Sport)

    name = CharField(_('league name'), max_length=60)

    min_age = SmallIntegerField(_('minimum age for signup'))
    max_age = SmallIntegerField(_('maximum age for signup'))

    gender = CharField(
        _('gender'),
        max_length=1,
        choices=GENDER_CHOICES,
        default=GENDER_UNDEFINED
    )
    # TODO: [MOD-02] A specialized class which handles calendars and schedules
    # should be created. The component should allow adding different schedules
    # for each country, league and sport.
    schedule = SmallIntegerField()

    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Division(Model):
    league = ForeignKey(League)

    level = SmallIntegerField(_('division level'))
    teams_num = SmallIntegerField(_('teams required'))

    name = CharField(_('division name'), max_length=30)

    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Manager(Model):
    """
    Represents the Player Character
    """
    user = ForeignKey(User)

    name = CharField(_('manager name'), max_length=60)
    age = SmallIntegerField(blank=True, null=True)
    gender = CharField(
        _('gender'),
        max_length=1,
        choices=GENDER_CHOICES,
        default=GENDER_UNDEFINED
    )

    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Club(Model):
    """
    Represents the main structure built, managed and developed by
    Player Characters through the game
    """
    manager = ForeignKey(Manager)
    country = ForeignKey(Country)

    name = CharField(_('club name'), max_length=60)

    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Team(Model):
    club = ForeignKey(Club)

    name = CharField(_('team name'), max_length=60)
    gender = CharField(
        _('gender'),
        max_length=1,
        choices=GENDER_CHOICES,
        default=GENDER_UNDEFINED
    )

    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class TeamDivision(Model):
    """
    A team can be registered in zero, one or more divisions
    """
    team = ForeignKey(Team)
    division = ForeignKey(Division)


class Match(Model):
    """
    A match is part of a division and can have teams playing it;
    it may be part of a division's round and season;
    all teams should be registered to the division the game is part of.
    """
    STATUS_SCHEDULED = 1
    STATUS_SIM_STARTED = 11
    STATUS_SIM_IN_PROGRESS = 12
    STATUS_SIM_FINISHED = 13
    STATUS_RENDER_STARTED = 22
    STATUS_RENDER_IN_PROGRESS = 23
    STATUS_RENDER_FINISHED = 23

    division = ForeignKey(Division)

    round = IntegerField(null=True, blank=True)
    season = IntegerField(null=True, blank=True)
    can_be_draw = BooleanField(default=True)
    # TODO: [MOD-03] Build a specialized class for stadiums
    # This should minimally know about name and capacity
    stadium = IntegerField(null=True, blank=True)

    # A JSON string, contains everything required to
    # render the game or restore a simulation
    journal = TextField(blank=True)
    # Tells whether simulation or rendering is currently running
    status = SmallIntegerField(default=1)
    # Number of minutes passed during rendering
    render_progress = SmallIntegerField(null=True, blank=True)

    date_scheduled = DateTimeField(_('scheduled on'), blank=True, null=True)
    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = _('matches')


class MatchTeam(Model):
    """
    Manages the adherence of a team to a certain match;
    includes tactics set for that match and outcome
    """
    TEAM_ROLE_HOME = 'home'
    TEAM_ROLE_AWAY = 'away'

    TEAM_ROLES = (
        (TEAM_ROLE_HOME, TEAM_ROLE_HOME),
        (TEAM_ROLE_AWAY, TEAM_ROLE_AWAY)
    )

    match = ForeignKey(Match)
    team = ForeignKey(Team)

    # The role of the team in the match
    role = CharField(_('team role'), max_length=10, choices=TEAM_ROLES)
    # Outcome of the game
    # For soccer, points represent goals scored during game
    points = SmallIntegerField(_('scored points'), default=0)
    # For soccer, reward represents the points awarded
    # for victory (i.e. 3p), or draw
    reward = SmallIntegerField(_('team reward'), default=0)

    # A JSON string, parsed when the match is initialized
    tactics = TextField(_('team tactics (json)'), default='{}')
    tactics_ref = TextField(
        _('team tactics reference'),
        editable=False,
        blank=True
    )

    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.tactics_ref = create_reference(self.tactics, self.match.pk)
        super().save(*args, **kwargs)

    def check_tactics_ref(self):
        # Checks that tactics data was saved correctly
        current_hash = create_reference(self.tactics, self.match.pk)
        if current_hash != self.tactics_ref:
            return False
        return True

    class Meta:
        verbose_name_plural = _('match teams')


class Attribute(Model):
    """
    Defines attributes that can possibly apply to game
    entities, such as the Manager or NPCs;
    """
    ATTR_TYPE_TRAIT = 1
    ATTR_TYPE_SKILL = 2
    APPLIES_TO_MANAGER = 'manager'
    APPLIES_TO_NPC = 'npc'

    sport = ForeignKey(Sport)

    name = CharField('attribute name', max_length=60)
    description = CharField('short description', max_length=250)
    applies_to = CharField(max_length=10)

    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ManagerAttribute(Model):
    """
    Holds the attributes assigned to each manager and their respective values
    """
    manager = ForeignKey(Manager)
    attribute = ForeignKey(Attribute)

    value = DecimalField(
        _('value of the attribute'),
        max_digits=16,
        decimal_places=4
    )

    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)


class Npc(Model):
    """
    Can be players, staff of a club; or anyone else who
    may have a role in the overall game;
    has a gender; may or may not belong to a club,
    may be in a club but not in a team (e.g. staff)
    """
    club = ForeignKey(Club, blank=True, null=True)
    team = ForeignKey(Team, blank=True, null=True)

    first_name = CharField(_('npc first name'), max_length=15)
    last_name = CharField(_('npc last name'), max_length=15)
    nickname = CharField(_('npc nickname'), max_length=20, blank=True)

    age = SmallIntegerField(blank=True, null=True)
    gender = CharField(
        _('gender'),
        max_length=1,
        choices=GENDER_CHOICES,
        default=GENDER_UNDEFINED
    )
    # TODO: [MOD-04] NPC roles should be formalized in a
    # separate table; also see MOD-01
    # It should be possible to extract the sport(s)
    # the Npc is relevat to from his role
    role = CharField(_('role'), max_length=20, blank=True)

    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)

    def __str__(self):
        if self.nickname != '':
            return '%s "%s" %s' % (
                self.first_name,
                self.nickname,
                self.last_name
            )
        return '%s %s' % (self.first_name, self.last_name)


class NpcAttribute(Model):
    npc = ForeignKey(Npc)
    attribute = ForeignKey(Attribute)

    value = DecimalField(
        _('value of the attribute'),
        max_digits=16,
        decimal_places=4
    )

    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)
