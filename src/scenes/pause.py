from tkinter import Canvas, PhotoImage
from assets import Assets, FontColor
from config import Config
from render import put_lines_centered
from .base import Scene, Pop, Transition


class Pause(Scene):
    def __init__(self, config: Config, assets: Assets) -> None:
        self.overlay = PhotoImage(file=config.overlay)
        self.assets = assets

    def update(self, dt: float, keys: set[str]) -> Transition:
        if "Escape" in keys:
            return Pop()
        return None

    def draw(self, canvas: Canvas) -> None:
        w, h = canvas.winfo_width(), canvas.winfo_height()
        title = self.assets.fonts.fit(h / 16)[FontColor.WHITE]
        sub = self.assets.fonts.fit(h / 32)[FontColor.BEIGE]
        canvas.create_image(0, 0, image=self.overlay, anchor="nw")
        put_lines_centered(
            [("Paused", title), ('Press "Escape" to Resume', sub)],
            canvas,
            w / 2,
            h / 2,
            gap=h / 32,
        )
