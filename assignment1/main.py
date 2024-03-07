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

def run_game_loop(lc,window):
    # Run one game
    lc.mainLoop(window, waitbot)

def main():
    # Set config file
    # config_name = "config_adv.yaml"
    config_name = "config3.yaml"
    cfg = read_config(config_name)
    waitBot = False

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
    # Initialize variables for overall wins
    total_player_wins = [0 for _ in range(cfg["no_of_players"])]

    # Outer Loop
    for round_number in range(1,101):
        print(f"Round {round_number}")

        # Run_game_round(lc,window)
        run_game_round(lc, window)

        # Update overall wins
        for i, player_win in enumerate(lc.get_winners()):
            total_player_wins[i] += player_win

    # Print the overall results
    print("\nOverall Results:")
    for i, total_wins in enumerate(total_player_wins):
        print(f"Player {i + 1} total wins: {total_wins}")

    # Quit Pygame and close the script
    pygame.quit()


if __name__ == "__main__":
    main()
