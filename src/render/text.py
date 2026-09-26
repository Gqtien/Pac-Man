from models import FrameBuffer
from PIL.Image import Image
from typing import TypeAlias
from assets import Font

Line: TypeAlias = tuple[str, Font]


def char_or_space(char: str, font: Font) -> str:
    try:
        font[char]
        return char
    except KeyError:
        return " "


def glyphs(text: str, font: Font) -> list[Image]:
    return [font[char_or_space(char, font)] for char in text.upper()]


def images_size(images: list[Image]) -> tuple[int, int]:
    width = sum(image.width for image in images)
    height = max((image.height for image in images), default=0)
    return width, height


def text_size(text: str, font: Font) -> tuple[int, int]:
    return images_size(glyphs(text, font))


def put_images(
    images: list[Image], framebuffer: FrameBuffer, x: int, y: int
) -> None:
    for image in images:
        framebuffer.put_image(image, x, y)
        x += image.width


def put_text(
    text: str, font: Font, framebuffer: FrameBuffer, x: int, y: int
) -> None:
    put_images(glyphs(text, font), framebuffer, x, y)


def put_text_centered(
    text: str, font: Font, framebuffer: FrameBuffer, x: int, y: int
) -> None:
    width, height = text_size(text, font)
    put_text(text, font, framebuffer, x - width // 2, y - height // 2)


def put_lines_centered(
    lines: list[Line],
    framebuffer: FrameBuffer,
    x: int | float,
    y: int | float,
    gap: int | float = 0
) -> None:
    x,  y, gap = int(x), int(y), int(gap)
    heights = [text_size(text, font)[1] for text, font in lines]
    top: int = y - (sum(heights) + gap * (len(lines) - 1)) // 2
    for (text, font), height in zip(lines, heights):
        put_text_centered(text, font, framebuffer, x, top + height // 2)
        top += height + gap
