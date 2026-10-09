from models import Keys
from scenes.factories import SceneFactories
from assets.font import LINES
from assets import Assets, FontColor
from storage import Config, save_score
from render import (
    FrameBuffer,
    Line,
    put_screen,
    text_font,
    title_font,
)
from .base import Scene, Transition, Reset


class EndScene(Scene):
    message: str
    color: FontColor

    def __init__(
        self,
        factories: SceneFactories,
        config: Config,
        assets: Assets,
        score: int,
    ) -> None:
        self.config = config
        self.assets = assets
        self.factories = factories
        self.score = score
        self.name_buffer: str = ""

    def update(self, dt: float, keys: set[int]) -> Transition:
        if Keys.Return in keys and self.name_buffer:
            save_score(
                self.config.highscore_path,
                self.name_buffer,
                self.score,
            )
            return Reset(self.factories.main(self.config, self.assets))
        if Keys.Backspace in keys:
            self.name_buffer = self.name_buffer[:-1]
        for code in keys:
            k = chr(code).upper()
            if len(k) != 1 or k not in "".join(LINES):
                continue
            self.name_buffer += k
            self.name_buffer = self.name_buffer[:10]
        return None

    def draw(self, framebuffer: FrameBuffer) -> None:
        title = title_font(framebuffer, self.assets, self.color)
        text = text_font(framebuffer, self.assets, FontColor.WHITE)
        lines: list[Line] = [
            (self.message, title),
            (f"Score - {self.score}", text),
            (f"Name:  {self.name_buffer:->10}", text),
            ('Press "Enter" to validate', text),
        ]
        framebuffer.clear()
        put_screen(framebuffer, lines)


class Lost(EndScene):
    message = "You Died"
    color = FontColor.RED


class Won(EndScene):
    message = "You Won !"
    color = FontColor.YELLOW
