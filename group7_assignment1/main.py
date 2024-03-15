# usr/bin/python3
"""
Script to start the game of Chinese Checkers.
"""
import pygame
import yaml
from gui.loops import LoopController
from gui.constants import WIDTH, HEIGHT


def read_config(file_name="config0.yaml"):
    # Read from YAML config file
    with open("config/" + file_name, "r") as file:
        cfg = yaml.safe_load(file)
    # Check config
    if len(cfg["player_list"]) != cfg["no_of_players"]:
        raise ValueError("Player count and types are not equal in config.")
    return cfg


def main():
    # Set config file
    # config_name = "config-mmcluster-greedy1.yaml"
    config_name = "config-mmcluster-greedy2.yaml"
    # config_name = "config-mmcluster-mmladder.yaml"
    # config_name = "config-mmladder-greedy2.yaml"
    cfg = read_config(config_name)

    waitBot = False  # True: bot waits for a key press before making a move

    # Initialize pygame window
    pygame.init()
    window = pygame.display.set_mode(
        (WIDTH, HEIGHT),
        pygame.SCALED | pygame.SRCALPHA,
    )
    pygame.display.set_caption("Chinese Checkers")

    # Enter game control loop
    lc = LoopController(cfg["player_list"])
    while True:
        lc.mainLoop(window, waitBot)


if __name__ == "__main__":
    main()
