from .base import Scene, Pop, Reset, Transition
from .factories import SceneFactories
from models import Keys
from assets import Assets, FontColor
from render import FrameBuffer, Line, put_screen, text_font, title_font
from storage import Config


class Pause(Scene):
    transparent = True

    def __init__(
        self, factories: SceneFactories, config: Config, assets: Assets
    ) -> None:
        self.factories = factories
        self.config = config
        self.assets = assets

    def update(self, dt: float, keys: set[int]) -> Transition:
        if Keys.Escape in keys:
            return Pop()
        if Keys.Return in keys:
            return Reset(self.factories.main(self.config, self.assets))
        return None

    def draw(self, framebuffer: FrameBuffer) -> None:
        title = title_font(framebuffer, self.assets, FontColor.WHITE)
        text = text_font(framebuffer, self.assets, FontColor.BEIGE)
        lines: list[Line] = [
            ("Paused", title),
            ('Press "Escape" to Resume', text),
            ('Or "Enter" to Exit', text),
        ]
        overlay = self.assets.overlay[framebuffer.width, framebuffer.height]
        framebuffer.put_image(overlay, 0, 0)
        put_screen(framebuffer, lines)
