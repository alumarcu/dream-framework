from django.db.models import Model, CharField


class Sport(Model):
    """
    Defines the types of sports that are available
    in a playable instance of dreamframework
    """
    SPORT_SOCCER_KEY = 'soccer'

    name = CharField(max_length=40)
    common_key = CharField(max_length=20, blank=True, default='')

    # TODO: [MOD-01] Correspondence between NPC roles and the sports they are
    # relevant to.
    # For example, it should be possible for a club to have the same medics
    # used for both the men's soccer team and women's handball. A Sport can
    # have multiple Roles associated (N to N assoc)

    def __str__(self):
        return self.name
