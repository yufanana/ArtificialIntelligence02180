# usr/bin/python3
"""
Script to start the game of Chinese Checkers.
"""
import hydra
import pygame
from gui.loops import LoopController
from gui.constants import WIDTH, HEIGHT


@hydra.main(version_base=None, config_path="config", config_name="config5.yaml")
def main(cfg):
    # Check config
    if len(cfg.player_list) != cfg.no_of_players:
        raise ValueError("Player count and types are not equal in config.")

    # Initialize pygame window
    pygame.init()
    window = pygame.display.set_mode(
        (WIDTH, HEIGHT), pygame.SCALED | pygame.SRCALPHA
    )
    pygame.display.set_caption("Chinese Checkers")

    # Enter game control loop
    lc = LoopController(cfg.player_list)
    while True:
        lc.mainLoop(window)


if __name__ == "__main__":
    main()
