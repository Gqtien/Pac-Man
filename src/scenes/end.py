from assets.font import LINES
from systems.highscore import load_highscore, save_highscore
from tkinter import Canvas
from assets import Assets, FontColor
from config import Config
from render import put_lines_centered
from .base import Scene, Pop, Transition
from abc import ABC, abstractmethod


class EndScene(Scene, ABC):
    def __init__(self, config: Config, assets: Assets, score: int) -> None:
        self.config = config
        self.assets = assets
        self.score = score
        self.highscore = load_highscore(config.highscore_filepath)
        self.name_buffer: str = ""
        if self.score >= self.highscore:
            # New highscore !
            self.highscore = self.score
            save_highscore(self.highscore, config.highscore_filepath)

    def update(self, dt: float, keys: set[str]) -> Transition:
        if "space" in keys:
            return Pop()
        if "BackSpace" in keys:
            self.name_buffer = self.name_buffer[:-1]
        for k in keys:
            k = k.upper() if k.isalpha() else k
            if len(k) != 1 or k not in ''.join(LINES):
                continue
            self.name_buffer += k
            self.name_buffer = self.name_buffer[:10]
        return None

    @abstractmethod
    def draw(self, canvas: Canvas) -> None:
        ...


class Death(EndScene):
    def draw(self, canvas: Canvas) -> None:
        canvas.delete("all")
        w, h = canvas.winfo_width(), canvas.winfo_height()
        title = self.assets.fonts.fit(h / 16)[FontColor.RED]
        sub = self.assets.fonts.fit(h / 32)[FontColor.WHITE]
        put_lines_centered(
            [
                ("You Died", title),
                (f"score - {self.score}", sub),
                (f"highscore - {self.highscore}", sub),
                ('Press "Space" to Retry', sub)
            ],
            canvas,
            w / 2,
            h / 2,
            gap=h / 32,
        )


class Win(EndScene):
    def draw(self, canvas: Canvas) -> None:
        canvas.delete("all")
        w, h = canvas.winfo_width(), canvas.winfo_height()
        title = self.assets.fonts.fit(h / 16)[FontColor.YELLOW]
        sub = self.assets.fonts.fit(h / 32)[FontColor.WHITE]
        put_lines_centered(
            [
                ("You Won !", title),
                (f"score - {self.score}", sub),
                (f"highscore - {self.highscore}", sub),
                (f"name:  {self.name_buffer:->10}", sub),
                ('Press "Space" to Retry', sub)
            ],
            canvas,
            w / 2,
            h / 2,
            gap=h / 32,
        )
