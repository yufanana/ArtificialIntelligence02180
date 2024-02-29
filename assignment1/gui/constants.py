"""
This file contains literals used in to create the GUI.

The following literals are defined:
- WIDTH: int
- HEIGHT: int
and other colours used.
"""

# from tkinter import Tk
# root = Tk()
# screen_w = int(root.winfo_screenwidth() * 0.9)
# screen_h = int(root.winfo_screenheight() * 0.9)
# root.destroy()
# del Tk

# Dynamic window size based on user's screen
# import sys
# from PySide6 import QtWidgets
# app = QtWidgets.QApplication(sys.argv)
# screen = app.primaryScreen()
# size = screen.size()

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

HEIGHT = 800
WIDTH = HEIGHT * 4 // 3
print(f"Creating GUI window of size ({WIDTH},{HEIGHT})")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (210, 43, 43)
GREEN = (0, 128, 0)
YELLOW = (255, 215, 0)
ORANGE = (252, 147, 3)
GRAY = (189, 189, 189)
LIGHT_GRAY = (228, 230, 231)
DARK_GRAY = (161, 166, 196)
PURPLE = (117, 10, 199)
PLAYER_COLORS = (YELLOW, RED, GREEN)
BG_RED = RED  # (235,160,160)
BG_GREEN = GREEN  # (0,200,0)
BG_YELLOW = YELLOW  # (255,238,144)
