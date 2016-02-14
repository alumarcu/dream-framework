from django.utils.translation import ugettext_lazy as _
from django.db.models import Model, CharField, BooleanField


class PlayerAction(Model):
    """
    Defines actions a FieldPlayer can perform during game
    """
    name = CharField(_('action name'), max_length=30)
    description = CharField(
        _('action description'),
        max_length=250,
        blank=True
    )

    # Whether the action can happen or is disabled
    enabled = BooleanField(_('action enabled'), default=False)

    def __str__(self):
        return self.name
