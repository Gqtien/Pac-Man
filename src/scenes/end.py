from models import Keys
from assets.font import LINES
from assets import Assets, FontColor
from storage import Config, save_score
from .base import Scene
from .events import Event, Leave
from systems import Outcome, Ending
from render import (
    FrameBuffer,
    Line,
    put_screen,
    text_font,
    title_font,
)


class End(Scene):
    def __init__(
        self,
        config: Config,
        assets: Assets,
        score: int,
        outcome: Ending,
    ) -> None:
        self.config = config
        self.assets = assets
        self.score = score
        self.outcome = outcome
        self.name_buffer: str = ""

    def update(self, dt: float, keys: set[int]) -> Event:
        if Keys.Escape in keys:
            return Leave()
        name = self.name_buffer.strip()
        if Keys.Return in keys and name:
            save_score(self.config.highscore_path, name, self.score)
            return Leave()
        if Keys.Backspace in keys:
            self.name_buffer = self.name_buffer[:-1]
        for code in keys:
            k = chr(code).upper() if code < 0x110000 else ""
            if len(k) != 1 or k not in "".join(LINES):
                continue
            self.name_buffer += k
            self.name_buffer = self.name_buffer[:10]
        return None

    def draw(self, framebuffer: FrameBuffer) -> None:
        message, color = self.banner()
        title = title_font(framebuffer, self.assets, color)
        text = text_font(framebuffer, self.assets, FontColor.WHITE)
        lines: list[Line] = [
            (message, title),
            (f"Score - {self.score}", text),
            (f"Name:  {self.name_buffer:->10}", text),
            ('Press "Enter" to validate', text),
            ('Or "Escape" to discard', text),
        ]
        framebuffer.clear()
        put_screen(framebuffer, lines)

    def banner(self) -> tuple[str, FontColor]:
        match self.outcome:
            case Outcome.WON:
                return "You Won !", FontColor.YELLOW
            case Outcome.LOST:
                return "Game Over !", FontColor.RED
            case Outcome.TIMED_OUT:
                return "Time's Up !", FontColor.ORANGE
