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


class Fonts(dict[tuple[FontColor, int], Font]):
    def __missing__(self, key: tuple[FontColor, int]) -> Font:
        color, scale = key
        font = self[key] = scale_font(self[color, 1], scale)
        return font


def load_fonts(sheet: SpriteSheet) -> Fonts:
    return Fonts({(color, 1): load_font(sheet, color) for color in FontColor})


def load_font(sheet: SpriteSheet, color: FontColor) -> Font:
    top = color.value * 4
    font = {
        char: sheet.sprite(col, top + row)
        for row, line in enumerate(LINES)
        for col, char in enumerate(line)
    }
    font[" "] = sheet.sprite(15, top)
    return font


def scale_font(font: Font, scale: int) -> Font:
    return {char: glyph.zoom(scale) for char, glyph in font.items()}
