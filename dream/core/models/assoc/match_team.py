from django.db.models import Model, CharField, DateTimeField, \
    ForeignKey, SmallIntegerField, TextField
from django.utils.translation import ugettext_lazy as _

from dream.tools import create_reference
from .. import Match, Team


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
