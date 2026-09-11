import time
from tkinter import Canvas, Event, Tk
from .base import Scene
from .main import Main
from models import Pop, Push, Reset, Transition


class SceneManager:
    def __init__(self) -> None:
        self.tk = Tk()
        self.canvas = Canvas(self.tk)
        self.canvas.pack(fill="both", expand=True)
        self.stack: list[Scene] = [Main()]
        self.last: float = time.perf_counter()
        self.keys: set[str] = set()
        self.tk.bind("<KeyPress>", self.on_key)
        self.tk.mainloop()

    @property
    def top(self) -> Scene:
        return self.stack[-1]

    def on_key(self, event: Event) -> None:
        self.keys.add(event.keysym)

    def tick(self) -> None:
        if not self.stack:
            self.tk.destroy()
            return
        now = time.perf_counter()
        dt, self.last = now - self.last, now
        keys, self.keys = self.keys, set()

        transition = self.top.update(dt, keys)
        self.apply(transition)
        if self.stack:
            self.top.draw(self.canvas)
        self.tk.after(16, self.tick)

    def apply(self, transition: Transition) -> None:
        match transition:
            case Push(scene):
                self.stack.append(scene)
            case Pop():
                self.stack.pop()
            case Reset(scene):
                self.stack = [scene]
            case None:
                pass
