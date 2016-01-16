from django.utils.translation import ugettext_lazy as _
from django.db.models import Model, CharField


class EngineParam(Model):

    section = CharField(_('section'), max_length=100, db_index=True)

    key = CharField(_('key'), max_length=250, unique=True, db_index=True)

    value = CharField(_('value'), max_length=250)

    description = CharField(
        _('description'),
        max_length=250,
        blank=True,
        default=''
    )

    def __str__(self):
        return '%s.%s = %s' % (self.section, self.key, self.value)
