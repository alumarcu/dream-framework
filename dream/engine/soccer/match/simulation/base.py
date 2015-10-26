from django.utils.translation import ugettext_lazy as _

from dream.engine.soccer.exceptions import InitError
from dream.tools import Logger


class BaseSimulation:
    def __init__(self):
        self._match_ids = []
        self.logger = Logger(__name__, Logger.default_message)

    # TODO: [SIM-02] Look into abstract classes in Python and decide whether its the case here
    # Possible example: http://zaiste.net/2013/01/abstract_classes_in_python/
    # Official docs: https://docs.python.org/3/library/abc.html
    def tactics_ok(self, tactics):
        # TODO: [SIM-01] Tactics validation
        return True

    def add_match(self, match_id):
        if type(match_id) is not int:
            raise InitError(_('Invalid match id supplied'))
        self._match_ids.append(match_id)

    def initialize(self):
        pass

    def loop(self):
        pass
