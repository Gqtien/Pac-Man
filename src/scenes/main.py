from tkinter import Canvas
from .transition import Transition, Push
from .base import Scene
from config import Config
from assets import Assets, FontColor
from .gameplay import Gameplay
from render import put_lines_centered


class Main(Scene):
    def __init__(self, config: Config, assets: Assets) -> None:
        self.config = config
        self.assets = assets

    def update(self, dt: float, keys: set[str]) -> Transition:
        if "space" in keys:
            return Push(Gameplay(self.config, self.assets))

    def draw(self, canvas: Canvas) -> None:
        canvas.delete("all")
        w, h = canvas.winfo_width(), canvas.winfo_height()
        title = self.assets.fonts.fit(h / 16)[FontColor.WHITE]
        sub = self.assets.fonts.fit(h / 32)[FontColor.BEIGE]
        put_lines_centered(
            [
                ("Pacman", title),
                ('Press "Space" to play', sub)
            ],
            canvas,
            w / 2,
            h / 2,
            gap=h / 32,
        )
