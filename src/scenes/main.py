from tkinter import Canvas
from .transition import Transition
from .base import Scene


class Main(Scene):
    def update(self, dt: float, keys: set[str]) -> Transition: ...

    def draw(self, canvas: Canvas) -> None: ...
