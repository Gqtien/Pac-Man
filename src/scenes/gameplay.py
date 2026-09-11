from tkinter import Canvas
from models import Transition
from .base import Scene


class Gameplay(Scene):
    def update(self, dt: float, keys: set[str]) -> Transition: ...

    def draw(self, canvas: Canvas) -> None: ...
