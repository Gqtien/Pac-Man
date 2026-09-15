from tkinter import Canvas
from assets import Font


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
