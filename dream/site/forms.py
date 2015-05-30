from django.forms import Form, CharField, PasswordInput, EmailField, ModelChoiceField, \
    ValidationError
from django.utils.translation import ugettext_lazy as _
from dream.core.models import Country


class SignupForm(Form):
    """
    Gathers all data required to initialize a manager, club and application user
    """
    username = CharField(label=_('username'), max_length=40)
    passwda = CharField(label=_('password'), max_length=60, widget=PasswordInput)
    passwdb = CharField(label=_('confirm password'), max_length=60, widget=PasswordInput)
    email = EmailField(label=_('e-mail'))

    # Country where the club should be created
    # TODO: [SIT-01] Default option should be
    # extracted from user's IP based location
    country = ModelChoiceField(label=_('country'), queryset=Country.objects.all())

    clubname = CharField(label=_('club name'), max_length=80)
    managername = CharField(label=_('manager name'), max_length=80)

    def clean_username(self):
        from django.contrib.auth.models import User

        # TODO: [FOR-01] Only alphanumeric and a few special
        # chars should be allowed in username
        # Currently, it's also possible to have usernames with
        # @ and dash, should be discussed if ok

        # Make sure the username is not already taken
        pickedusername = self.cleaned_data.get('username')
        if User.objects.filter(username=pickedusername).exists():
            raise ValidationError(_('username already taken'))

        return pickedusername

    def clean_passwdb(self):
        passwda = self.cleaned_data.get('passwda')
        passwdb = self.cleaned_data.get('passwdb')

        if not passwdb:
            raise ValidationError(_('please confirm password'))

        if passwda != passwda:
            raise ValidationError(_('passwords do not match'))

        if len(passwdb) < 6:
            raise ValidationError(_('password should have at least 6 characters'))

        return passwdb
