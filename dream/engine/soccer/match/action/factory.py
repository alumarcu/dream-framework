from django.utils.translation import ugettext_lazy as _

from dream.engine.soccer.exceptions import LoopError
from .actions import *


class ActionFactory:

    def __init__(self):
        self._map = {
            'Pass': PassAction,
            'Indirect_Kick_Pass': IndirectKickPassAction,
            'Move_Defensive': DefensivePositionAction,
            'Move_Offensive': OffensivePositionAction
        }

    @staticmethod
    def get():
        if not hasattr(ActionFactory, 'instance'):
            ActionFactory.instance = ActionFactory()
        return ActionFactory.instance

    def create_action(self, class_name):
        if class_name not in self._map:
            LoopError(_('Invalid class name %s' % class_name))
        return self._map[class_name]
