from pygame.locals import *
from abc import ABC, ABCMeta, abstractmethod

from gui.literals import *
from gui.gui_helpers import *

from .game import *
from .piece import *
from .helpers import *


class PlayerMeta(ABCMeta):
    playerTypes = []

    def __init__(cls, name, bases, attrs):
        if ABC not in bases:
            PlayerMeta.playerTypes.append(cls)
        super().__init__(name, bases, attrs)


class Player(ABC, metaclass=PlayerMeta):
    def __init__(self):
        self.playerNum = 0
        self.has_won = False

    def getPlayerNum(self):
        return self.playerNum

    def setPlayerNum(self, num: int):
        self.playerNum = num

    @abstractmethod
    def pickMove(self, g: Game):
        ...

