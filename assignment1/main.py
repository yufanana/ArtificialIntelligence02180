# usr/bin/python3
"""
Script to start the game of Chinese Checkers.
"""
import pygame
from gui.loops import LoopController
from gui.constants import WIDTH, HEIGHT

# from game_logic.human import HumanPlayer
from bots.GreedyBot0 import GreedyBot0
from bots.GreedyBot1 import GreedyBot1
from bots.GreedyBot2 import GreedyBot2
from bots.RandomBot import RandomBot


def main():
    # Initialize pygame window
    pygame.init()
    window = pygame.display.set_mode(
        (WIDTH, HEIGHT), pygame.SCALED | pygame.SRCALPHA
    )
    pygame.display.set_caption("Chinese Checkers")

    # Initialize type of players
    playerList = [
        RandomBot(),
        GreedyBot0(),
        GreedyBot1(),
        GreedyBot2(),
    ]

    # Enter game control loop
    lc = LoopController(playerList)
    while True:
        lc.mainLoop(window)


if __name__ == "__main__":
    main()
