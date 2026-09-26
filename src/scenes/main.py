from models import FrameBuffer
from PIL.Image import Image
from .base import Scene, Transition, Push, Pop
from config import Config
from assets import Assets, FontColor
from scenes.factories import SceneFactories
from render import put_lines_centered
from systems.highscore import load_highscore, HighScore


class Main(Scene):
    def __init__(
            self, factories: SceneFactories, config: Config, assets: Assets
    ) -> None:
        self.config = config
        self.assets = assets
        self.factories = factories
        self.highscore: HighScore = load_highscore(config.highscore_filepath)

    def update(self, dt: float, keys: set[str]) -> Transition:
        if "q" in keys:
            return Pop()
        if " " in keys:
            return Push(
                self.factories.gameplay(self.config, self.assets)
            )
        return None

    def draw(self, framebuffer: FrameBuffer) -> None:
        color_bytes = b"\x00\x00\x00\xFF"
        framebuffer.clear(color_bytes)
        w, h = framebuffer.width, framebuffer.height
        title = self.assets.fonts.fit(h / 16)[FontColor.YELLOW]
        sub = self.assets.fonts.fit(h / 32)[FontColor.WHITE]
        highscore_table = self.assets.fonts.fit(h / 32)[FontColor.CYAN]
        lines:  list[tuple[str, dict[str, Image]]] = [("Pacman", title)]
        lines.append(("", title))
        lines.extend(
            (f"{name:10} - {score:07}", highscore_table)
            for name, score in self.highscore.items()
        )
        lines.append(("", title))
        lines.append(('Press "Space" to play', sub))
        put_lines_centered(
            lines,
            framebuffer,
            w / 2,
            h / 2,
            gap=h / 32,
        )
