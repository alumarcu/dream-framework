from django.db.models import Model, ForeignKey
from .. import Team, Division


class TeamDivision(Model):
    """
    A Team can be registered in zero, one or more Divisions
    """
    team = ForeignKey(Team)
    division = ForeignKey(Division)
