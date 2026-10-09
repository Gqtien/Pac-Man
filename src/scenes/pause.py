from models import FrameBuffer
from assets import Assets, FontColor
from config import Config
from render import put_lines_centered
from .base import Scene, Pop, Transition
from PIL.Image import Image, open as open_image


class Pause(Scene):
    def __init__(self, config: Config, assets: Assets) -> None:
        with open_image(config.overlay) as img:
            img.load()
        self.overlay: Image = img
        self.assets = assets

    def update(self, dt: float, keys: set[str]) -> Transition:
        if "Escape" in keys:
            return Pop()
        return None

    def draw(self, framebuffer: FrameBuffer) -> None:
        w, h = framebuffer.width, framebuffer.height
        title = self.assets.fonts.fit(h / 16)[FontColor.WHITE]
        sub = self.assets.fonts.fit(h / 32)[FontColor.BEIGE]
        framebuffer.put_image(self.overlay, 0, 0)
        put_lines_centered(
            [("Paused", title), ('Press "Escape" to Resume', sub)],
            framebuffer,
            w / 2,
            h / 2,
            gap=h / 32,
        )
