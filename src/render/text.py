from typing import TypeAlias
from PIL.Image import Image
from assets import Assets, Font, FontColor
from .framebuffer import FrameBuffer
from .images import images_size, put_images

Line: TypeAlias = tuple[str, Font]


def glyphs(text: str, font: Font) -> list[Image]:
    return [font.get(char, font[" "]) for char in text.upper()]


def text_size(text: str, font: Font) -> tuple[int, int]:
    return images_size(glyphs(text, font))


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
    x: float,
    y: float,
    gap: float = 0,
) -> None:
    x, y, gap = int(x), int(y), int(gap)
    heights = [text_size(text, font)[1] for text, font in lines]
    top: int = y - (sum(heights) + gap * (len(lines) - 1)) // 2
    for (text, font), height in zip(lines, heights):
        put_text_centered(text, font, framebuffer, x, top + height // 2)
        top += height + gap


def title_font(
    framebuffer: FrameBuffer, assets: Assets, color: FontColor
) -> Font:
    return assets.fonts.fit(framebuffer.height / 16)[color]


def text_font(
    framebuffer: FrameBuffer, assets: Assets, color: FontColor
) -> Font:
    return assets.fonts.fit(framebuffer.height / 32)[color]


def put_screen(framebuffer: FrameBuffer, lines: list[Line]) -> None:
    w, h = framebuffer.width, framebuffer.height
    put_lines_centered(lines, framebuffer, w / 2, h / 2, gap=h / 32)
