# from tkinter import Tk
# root = Tk()
# screen_w = int(root.winfo_screenwidth() * 0.9)
# screen_h = int(root.winfo_screenheight() * 0.9)
# root.destroy()
# del Tk
import sys
from PySide6 import QtWidgets

app = QtWidgets.QApplication(sys.argv)
screen = app.primaryScreen()
size = screen.size()

# Dynamic window size based on user's screen
# screen_w = size.width()
# screen_h = size.height()
# print(f"width: {screen_w}, height: {screen_h}")

# # Enforce aspect ratio of 4:3
# if int(screen_w * (3/4)) <= screen_h:
#     WIDTH = screen_w
#     HEIGHT = int(screen_w * (3/4))
# else:
#     HEIGHT = screen_h
#     WIDTH = int(screen_h * (4/3))
# del screen_w, screen_h

WIDTH = 800
HEIGHT = 600
print(f"width: {WIDTH}, height: {HEIGHT}")


# Key: playerNum, Value: set of start coordinates
START_COOR = {
    1: {
        (3, -5),
        (1, -4),
        (4, -6),
        (1, -5),
        (4, -7),
        (2, -6),
        (4, -4),
        (3, -6),
        (0, -4),
        (4, -5),
        (3, -7),
        (2, -4),
        (4, -8),
        (3, -4),
        (2, -5),
    },
    2: {
        (-4, 4),
        (-5, 1),
        (-4, 1),
        (-5, 4),
        (-7, 4),
        (-6, 4),
        (-4, 0),
        (-5, 3),
        (-4, 3),
        (-5, 2),
        (-7, 3),
        (-4, 2),
        (-6, 3),
        (-8, 4),
        (-6, 2),
    },
    3: {
        (4, 4),
        (2, 4),
        (4, 0),
        (0, 4),
        (3, 4),
        (4, 1),
        (3, 1),
        (4, 3),
        (1, 4),
        (4, 2),
        (2, 3),
        (3, 3),
        (2, 2),
        (3, 2),
        (1, 3),
    },
}

# Key: playerNum, Value: set of end coordinates
END_COOR = {
    3: {
        (-4, -2),
        (-4, -1),
        (-3, -2),
        (-3, -1),
        (-2, -2),
        (-4, -3),
        (-3, -3),
        (-4, 0),
        (-2, -3),
        (-1, -3),
        (0, -4),
        (-1, -4),
        (-4, -4),
        (-3, -4),
        (-2, -4),
    },
    2: {
        (6, -4),
        (4, 0),
        (4, -3),
        (7, -3),
        (5, -2),
        (5, -1),
        (6, -2),
        (4, -4),
        (5, -3),
        (6, -3),
        (7, -4),
        (8, -4),
        (4, -1),
        (4, -2),
        (5, -4),
    },
    1: {
        (-4, 4),
        (-3, 4),
        (0, 4),
        (-4, 7),
        (-2, 4),
        (-3, 7),
        (-1, 4),
        (-1, 5),
        (-4, 6),
        (-3, 6),
        (-2, 6),
        (-4, 5),
        (-3, 5),
        (-4, 8),
        (-2, 5),
    },
}

# Set of neutral coordinates in the middle of the board
NEUTRAL_COOR = {
    (3, -2),
    (3, -1),
    (-3, 0),
    (-3, 3),
    (0, 2),
    (1, -3),
    (1, 0),
    (-2, -1),
    (-1, -2),
    (-1, -1),
    (-2, 1),
    (-1, 1),
    (3, -3),
    (3, 0),
    (-3, 2),
    (0, -1),
    (0, -2),
    (0, 1),
    (2, -2),
    (2, -1),
    (1, 2),
    (2, 1),
    (-2, 0),
    (-1, 0),
    (-2, 3),
    (-1, 3),
    (-2, 2),
    (0, -3),
    (-3, 1),
    (0, 0),
    (2, -3),
    (1, 1),
    (0, 3),
    (2, 0),
    (1, -2),
    (1, -1),
    (-1, 2),
}

# All possible coordinates on the board
ALL_COOR = (
    END_COOR[1]
    | END_COOR[2]
    | END_COOR[3]
    | START_COOR[1]
    | START_COOR[2]
    | START_COOR[3]
    | NEUTRAL_COOR
)

# Unit vectors for the 6 directions from a cell
DIRECTIONS = {(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)}

POINTS = (
    (-4, 7),
    (-3, 7),
    (-4, 6),
    (-2, 6),
    (-4, 5),
    (-1, 5),
    (-8, 4),
    (4, 4),
    (-7, 3),
    (4, 3),
    (-6, 2),
    (4, 2),
    (-5, 1),
    (4, 1),
    (-4, 0),
    (4, 0),
    (-4, -1),
    (5, -1),
    (-4, -2),
    (6, -2),
    (-4, -3),
    (7, -3),
    (-4, -4),
    (8, -4),
    (1, -5),
    (4, -5),
    (2, -6),
    (4, -6),
    (3, -7),
    (4, -7),
    (-7, 3),
    (-7, 4),
    (-6, 2),
    (-6, 4),
    (-5, 1),
    (-5, 4),
    (-4, -4),
    (-4, 8),
    (-3, -4),
    (-3, 7),
    (-2, -4),
    (-2, 6),
    (-1, -4),
    (-1, 5),
    (0, -4),
    (0, 4),
    (1, -5),
    (1, 4),
    (2, -6),
    (2, 4),
    (3, -7),
    (3, 4),
    (4, -8),
    (4, 4),
    (5, -4),
    (5, -1),
    (6, -4),
    (6, -2),
    (7, -4),
    (7, -3),
    (3, 4),
    (4, 3),
    (2, 4),
    (4, 2),
    (1, 4),
    (4, 1),
    (-4, 8),
    (8, -4),
    (-4, 7),
    (7, -4),
    (-4, 6),
    (6, -4),
    (-4, 5),
    (5, -4),
    (-4, 4),
    (4, -4),
    (-5, 4),
    (4, -5),
    (-6, 4),
    (4, -6),
    (-7, 4),
    (7, -4),
    (-8, 4),
    (4, -8),
    (-4, -1),
    (-1, -4),
    (-4, -2),
    (-2, -4),
    (-4, -3),
    (-3, -4),
)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (210, 43, 43)
GREEN = (0, 128, 0)
YELLOW = (255, 215, 0)
ORANGE = (252, 147, 3)
GRAY = (189, 189, 189)
LIGHT_GRAY = (228, 230, 231)
PLAYER_COLORS = (YELLOW, RED, GREEN)
BG_RED = RED  # (235,160,160)
BG_GREEN = GREEN  # (0,200,0)
BG_YELLOW = YELLOW  # (255,238,144)
