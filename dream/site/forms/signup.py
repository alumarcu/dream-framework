from django.utils.translation import ugettext_lazy as _
from django.forms import Form, CharField, PasswordInput, EmailField, ModelChoiceField, \
    ValidationError

from dream.core.models import Country


class SignupForm(Form):
    """
    Filled to create a new account
    """
    username = CharField(label=_('username'), max_length=40)
    password = CharField(
        label=_('password'),
        max_length=60,
        widget=PasswordInput
    )
    password_confirmed = CharField(
        label=_('confirm password'),
        max_length=60,
        widget=PasswordInput
    )
    email = EmailField(label=_('e-mail'))

    # Country where the club should be created
    # TODO: [SIT-01] Default option should be
    # extracted from user's IP based location
    country = ModelChoiceField(label=_('country'), queryset=Country.objects.all())

    club_name = CharField(label=_('club name'), max_length=80)
    manager_name = CharField(label=_('manager name'), max_length=80)

    def clean_username(self):
        from django.contrib.auth.models import User

        # TODO: [FOR-01] Only alphanumeric and a few special
        # chars should be allowed in username
        # Currently, it's also possible to have username with
        # @ and dash, should be discussed if ok

        # Make sure the username is not already taken
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError(_('username already taken'))

        return username

    def clean_password_confirmed(self):
        password = self.cleaned_data.get('password')
        password_confirmed = self.cleaned_data.get('password_confirmed')

        if not password_confirmed:
            raise ValidationError(_('please confirm password'))

        if password != password_confirmed:
            raise ValidationError(_('password confirmation does not match password'))

        if len(password) < 6:
            raise ValidationError(_('password should have at least 6 characters'))

        return password
