from tkinter import Canvas
from .transition import Pop, Transition
from .base import Scene


class Pause(Scene):
    def update(self, dt: float, keys: set[str]) -> Transition:
        if "Escape" in keys:
            return Pop()
        return None

    def draw(self, canvas: Canvas) -> None:
        canvas.delete("all")
        canvas.create_text(
            50, 50,
            text="Pause",
            fill="black",
            font=("Arial", 20)
        )
