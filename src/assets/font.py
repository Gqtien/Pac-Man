from enum import Enum
from tkinter import PhotoImage
from typing import TypeAlias
from .sheet import SpriteSheet

Font: TypeAlias = dict[str, PhotoImage]

LINES = (
    "ABCDEFGHIJKLMNO",
    "PQRSTUVWXYZ!©pts",
    '0123456789/-"',
)


class FontColor(Enum):
    WHITE = 0
    RED = 1
    PINK = 2
    CYAN = 3
    ORANGE = 4
    BEIGE = 5
    YELLOW = 6


Fonts: TypeAlias = dict[FontColor, Font]


def load_fonts(sheet: SpriteSheet) -> Fonts:
    return {color: load_font(sheet, color) for color in FontColor}


def load_font(sheet: SpriteSheet, color: FontColor) -> Font:
    top = color.value * 4
    font = {
        char: sheet.sprite(col, top + row)
        for row, line in enumerate(LINES)
        for col, char in enumerate(line)
    }
    font[" "] = sheet.sprite(15, top)
    return font
