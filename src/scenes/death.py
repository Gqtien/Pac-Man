from systems.highscore import load_highscore, save_highscore
from tkinter import Canvas
from assets import Assets, FontColor
from config import Config
from render import put_lines_centered
from .base import Scene, Pop, Transition


class Death(Scene):
    def __init__(self, config: Config, assets: Assets, score: int) -> None:
        self.config = config
        self.assets = assets
        self.score = score
        self.highscore = load_highscore(config.highscore_filepath)
        if self.score >= self.highscore:
            # New highscore !
            self.highscore = self.score
            save_highscore(self.highscore, config.highscore_filepath)

    def update(self, dt: float, keys: set[str]) -> Transition:
        if "space" in keys:
            return Pop()
        return None

    def draw(self, canvas: Canvas) -> None:
        canvas.delete("all")
        w, h = canvas.winfo_width(), canvas.winfo_height()
        title = self.assets.fonts.fit(h / 16)[FontColor.WHITE]
        sub = self.assets.fonts.fit(h / 32)[FontColor.BEIGE]
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
