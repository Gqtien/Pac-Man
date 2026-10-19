from enum import Enum, auto
from .events import Event, Start, Quit
from .base import Scene
from models import Keys
from storage import Config, load_highscores
from assets import Assets, FontColor
from render import (
    FrameBuffer,
    Line,
    put_screen,
    text_font,
    title_font,
)


class Mode(Enum):
    HIGHSCORES = auto()
    CONTROLS = auto()

    def shift(self, step: int) -> "Mode":
        members = list(type(self))
        return members[(members.index(self) + step) % len(members)]


class Main(Scene):
    def __init__(self, config: Config, assets: Assets) -> None:
        self.config = config
        self.assets = assets
        self.highscores = load_highscores(config.highscore_path)
        self.mode = Mode.HIGHSCORES

    def update(self, dt: float, keys: set[int]) -> Event:
        if Keys.Q in keys:
            return Quit()
        if Keys.Space in keys:
            return Start()
        if Keys.Left in keys:
            self.mode = self.mode.shift(-1)
        if Keys.Right in keys:
            self.mode = self.mode.shift(1)
        return None

    def draw(self, framebuffer: FrameBuffer) -> None:
        title = title_font(framebuffer, self.assets, FontColor.YELLOW)
        table = text_font(framebuffer, self.assets, FontColor.CYAN)
        text = text_font(framebuffer, self.assets, FontColor.WHITE)
        name, rows = self.page()
        lines: list[Line] = [(f"<  {name}  >", title), ("", title)]
        lines.extend((row, table) for row in rows)
        lines.append(("", title))
        lines.append(('Press "Space" to play', text))
        framebuffer.clear()
        put_screen(framebuffer, lines)

    def page(self) -> tuple[str, list[str]]:
        match self.mode:
            case Mode.HIGHSCORES:
                return "Pacman", [
                    f"{name:10} - {score:07}"
                    for name, score in self.highscores.items()
                ]
            case Mode.CONTROLS:
                invincible_key = self.config.cheat_invincible_key.name
                freeze_key = self.config.cheat_freeze_ghosts_key.name
                win_key = self.config.cheat_win_key.name
                return "Controls", [
                    "↑↓←→: Up/Down/Left/Right",
                    "Escape: Pause",
                    "Q: Exit Game",
                    f"{invincible_key}: Toggle Invincibility",
                    f"{freeze_key}: Toggle Ghosts Freeze",
                    f"{win_key}: Skip to Next Level",
                ]
