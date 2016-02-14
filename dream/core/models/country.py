from django.db.models import Model, CharField, DateTimeField
from django.utils.translation import ugettext_lazy as _


class Country(Model):
    """
    Countries define the way the users are grouped;
    it is not required that real countries are used
    """
    name = CharField(_('country name'), max_length=60)
    country_code = CharField(_('country iso code'), max_length=5)

    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = _('countries')
