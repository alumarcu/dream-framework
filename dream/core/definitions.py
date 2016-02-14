from django.utils.translation import ugettext_lazy as _

"""
Gender constants
"""
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
