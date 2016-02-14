from abc import ABCMeta, abstractmethod


class Action(metaclass=ABCMeta):
    """
    Define basic methods for objects implementing player action logic

    :type player: dream.engine.soccer.match.actors.FieldPlayer|None
    :type board: dream.engine.soccer.match.board.Board|None
    """
    def __init__(self):
        self.player = None
        self.board = None

    @abstractmethod
    def perform(self):
        pass

    @abstractmethod
    def check_dependencies(self):
        pass
