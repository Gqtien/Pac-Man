from models import FrameBuffer
from scenes.factories import SceneFactories
from assets.font import LINES
from assets import Assets, FontColor
from storage import Config, save_score
from render import put_lines_centered
from .base import Scene, Transition, Reset
from abc import ABC
from PIL.Image import Image


class EndScene(Scene, ABC):
    def __init__(
            self,
            factories: SceneFactories,
            config: Config,
            assets: Assets,
            score: int
    ) -> None:
        self.config = config
        self.assets = assets
        self.factories = factories
        self.score = score
        self.name_buffer: str = ""

    def update(self, dt: float, keys: set[str]) -> Transition:
        if "Return" in keys and self.name_buffer:
            save_score(
                self.config.highscore_filepath,
                self.name_buffer,
                self.score,
            )
            return Reset(self.factories.main(self.config, self.assets))
        if "BackSpace" in keys:
            self.name_buffer = self.name_buffer[:-1]
        for k in keys:
            k = k.upper() if k.isalpha() else k
            if len(k) != 1 or k not in ''.join(LINES):
                continue
            self.name_buffer += k
            self.name_buffer = self.name_buffer[:10]
        return None


class Death(EndScene):
    def draw(self, framebuffer: FrameBuffer) -> None:
        framebuffer.clear(b"\x00\x00\x00\xFF")
        w, h = framebuffer.width, framebuffer.height
        title = self.assets.fonts.fit(h / 16)[FontColor.RED]
        sub = self.assets.fonts.fit(h / 32)[FontColor.WHITE]
        lines:  list[tuple[str, dict[str, Image]]] = [
            ("You Died", title),
            (f"Score - {self.score}", sub),
            (f"Name:  {self.name_buffer:->10}", sub),
            ('Press "Enter" to validate', sub),
        ]
        put_lines_centered(lines, framebuffer, w / 2, h / 2, gap=h / 32)


class Win(EndScene):
    def draw(self, framebuffer: FrameBuffer) -> None:
        framebuffer.clear(b"\x00\x00\x00\xFF")
        w, h = framebuffer.width, framebuffer.height
        title = self.assets.fonts.fit(h / 16)[FontColor.YELLOW]
        sub = self.assets.fonts.fit(h / 32)[FontColor.WHITE]
        lines: list[tuple[str, dict[str, Image]]] = [
            ("You Won !", title),
            (f"Score - {self.score}", sub),
            (f"Name:  {self.name_buffer:->10}", sub),
            ('Press "Enter" to validate', sub),
        ]
        put_lines_centered(lines, framebuffer, w / 2, h / 2, gap=h / 32)
