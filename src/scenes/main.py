from models import Keys
from .base import Scene, Transition, Push, Pop
from storage import Config, load_highscores
from assets import Assets, FontColor
from scenes.factories import SceneFactories
from render import (
    FrameBuffer,
    Line,
    put_screen,
    text_font,
    title_font,
)


class Main(Scene):
    def __init__(
            self, factories: SceneFactories, config: Config, assets: Assets
    ) -> None:
        self.config = config
        self.assets = assets
        self.factories = factories
        self.highscores = load_highscores(config.highscore_path)

    def update(self, dt: float, keys: set[int]) -> Transition:
        if Keys.Q in keys:
            return Pop()
        if Keys.Space in keys:
            return Push(
                self.factories.gameplay(self.config, self.assets)
            )
        return None

    def draw(self, framebuffer: FrameBuffer) -> None:
        title = title_font(framebuffer, self.assets, FontColor.YELLOW)
        table = text_font(framebuffer, self.assets, FontColor.CYAN)
        text = text_font(framebuffer, self.assets, FontColor.WHITE)
        lines: list[Line] = [("Pacman", title), ("", title)]
        lines.extend(
            (f"{name:10} - {score:07}", table)
            for name, score in self.highscores.items()
        )
        lines.append(("", title))
        lines.append(('Press "Space" to play', text))
        framebuffer.clear()
        put_screen(framebuffer, lines)
