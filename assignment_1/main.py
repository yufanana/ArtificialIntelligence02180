import pygame
from gui.loops import *
from game_logic.game import *
from game_logic.player import *
from gui.literals import *

from bots import *

pygame.init()
window = pygame.display.set_mode(
    (WIDTH, HEIGHT), pygame.SCALED | pygame.SRCALPHA
)
pygame.display.set_caption("Chinese Checkers")

lc = LoopController()

while True:
    """
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit() """
    lc.mainLoop(window)
