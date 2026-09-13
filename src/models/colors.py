from enum import Enum


class Color(str, Enum):
    PACMAN = "yellow"
    BLINKY = "red"
    PINKY = "pink"
    INKY = "cyan"
    CLYDE = "orange"
    WALL = "darkblue"
    WALL_OUTLINE = "blue"
