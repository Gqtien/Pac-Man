from tkinter import Canvas, PhotoImage
from assets import Assets, FontColor
from config import Config
from render import put_text_centered
from .base import Scene
from .transition import Pop, Transition


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
        font = self.assets.fonts.fit(h / 16)[FontColor.WHITE]
        canvas.create_image(0, 0, image=self.overlay, anchor="nw")
        put_text_centered("PAUSE", font, canvas, w / 2, h / 2)
