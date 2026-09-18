from tkinter import Canvas, PhotoImage
from typing import TypeAlias
from assets import Font

Line: TypeAlias = tuple[str, Font]


def char_or_space(char: str, font: Font) -> str:
    try:
        font[char]
        return char
    except KeyError:
        return " "


def glyphs(text: str, font: Font) -> list[PhotoImage]:
    return [font[char_or_space(char, font)] for char in text.upper()]


def images_size(images: list[PhotoImage]) -> tuple[int, int]:
    width = sum(image.width() for image in images)
    height = max((image.height() for image in images), default=0)
    return width, height


def text_size(text: str, font: Font) -> tuple[int, int]:
    return images_size(glyphs(text, font))


def put_images(
    images: list[PhotoImage], canvas: Canvas, x: float, y: float
) -> None:
    for image in images:
        canvas.create_image(x, y, image=image, anchor="nw")
        x += image.width()


def put_text(
    text: str, font: Font, canvas: Canvas, x: float, y: float
) -> None:
    put_images(glyphs(text, font), canvas, x, y)


def put_text_centered(
    text: str, font: Font, canvas: Canvas, x: float, y: float
) -> None:
    width, height = text_size(text, font)
    put_text(text, font, canvas, x - width / 2, y - height / 2)


def put_lines_centered(
    lines: list[Line], canvas: Canvas, x: float, y: float, gap: float = 0.0
) -> None:
    heights = [text_size(text, font)[1] for text, font in lines]
    top = y - (sum(heights) + gap * (len(lines) - 1)) / 2
    for (text, font), height in zip(lines, heights):
        put_text_centered(text, font, canvas, x, top + height / 2)
        top += height + gap
