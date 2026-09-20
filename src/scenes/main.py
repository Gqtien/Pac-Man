from tkinter import Canvas
from .transition import Transition, Push
from .base import Scene
from config import Config
from assets import Assets
from .gameplay import Gameplay


class Main(Scene):
    def __init__(self, config: Config, assets: Assets) -> None:
        self.config = config
        self.assets = assets

    def update(self, dt: float, keys: set[str]) -> Transition:
        if "space" in keys:
            return Push(Gameplay(self.config, self.assets))

    def draw(self, canvas: Canvas) -> None: ...
