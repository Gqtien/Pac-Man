from tkinter import Canvas
from assets import Assets, FontColor
from config import Config
from render import put_lines_centered
from .base import Scene
from .transition import Pop, Transition


class Death(Scene):
    def __init__(self, config: Config, assets: Assets) -> None:
        self.config = config
        self.assets = assets

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
            [("You Died", title), ('Press "Space" to Retry', sub)],
            canvas,
            w / 2,
            h / 2,
            gap=h / 32,
        )
