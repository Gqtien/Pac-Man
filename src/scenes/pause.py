from models import Keys
from assets import Assets, FontColor
from render import FrameBuffer, Line, put_screen, text_font, title_font
from .base import Scene, Pop, Transition


class Pause(Scene):
    transparent = True

    def __init__(self, assets: Assets) -> None:
        self.assets = assets

    def update(self, dt: float, keys: set[int]) -> Transition:
        if Keys.Escape in keys:
            return Pop()
        return None

    def draw(self, framebuffer: FrameBuffer) -> None:
        title = title_font(framebuffer, self.assets, FontColor.WHITE)
        text = text_font(framebuffer, self.assets, FontColor.BEIGE)
        lines: list[Line] = [
            ("Paused", title),
            ('Press "Escape" to Resume', text),
        ]
        overlay = self.assets.overlay[framebuffer.width, framebuffer.height]
        framebuffer.put_image(overlay, 0, 0)
        put_screen(framebuffer, lines)
