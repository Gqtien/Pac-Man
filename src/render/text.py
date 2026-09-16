from tkinter import Canvas
from typing import TypeAlias
from assets import Font

Line: TypeAlias = tuple[str, Font]


def char_or_space(char: str, font: Font) -> str:
    try:
        font[char]
        return char
    except KeyError:
        return " "


def text_size(text: str, font: Font) -> tuple[int, int]:
    glyphs = [font[char_or_space(char, font)] for char in text]
    width = sum(glyph.width() for glyph in glyphs)
    height = max((glyph.height() for glyph in glyphs), default=0)
    return width, height


def put_text(
    text: str, font: Font, canvas: Canvas, x: float, y: float
) -> None:
    upper = text.upper()
    for char in upper:
        glyph = font[char_or_space(char, font)]
        canvas.create_image(x, y, image=glyph, anchor="nw")
        x += glyph.width()


def put_text_centered(
    text: str, font: Font, canvas: Canvas, x: float, y: float
) -> None:
    upper = text.upper()
    width, height = text_size(upper, font)
    put_text(upper, font, canvas, x - width / 2, y - height / 2)


def put_lines_centered(
    lines: list[Line], canvas: Canvas, x: float, y: float, gap: float = 0.0
) -> None:
    heights = [text_size(text, font)[1] for text, font in lines]
    top = y - (sum(heights) + gap * (len(lines) - 1)) / 2
    for (text, font), height in zip(lines, heights):
        put_text_centered(text, font, canvas, x, top + height / 2)
        top += height + gap
