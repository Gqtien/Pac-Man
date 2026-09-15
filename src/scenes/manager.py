import time
from tkinter import Canvas, Event, Tk
from .base import Scene
from .transition import Pop, Push, Reset, Transition


class SceneManager:
    def __init__(self) -> None:
        self.tk = Tk()
        self.canvas = Canvas(self.tk, bg="black")
        self.canvas.pack(fill="both", expand=True)
        self.stack: list[Scene] = []
        self.last: float = time.perf_counter()
        self.keys: set[str] = set()
        self.tk.bind("<KeyPress>", self.on_key)
        self.tk.after(0, self.tick)

    def start(self, initial_scene: Scene) -> None:
        self.stack.append(initial_scene)
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
        self.canvas.delete("all")
        now = time.perf_counter()
        dt, self.last = now - self.last, now
        keys, self.keys = self.keys, set()

        transition = self.top.update(dt, keys)
        self.apply(transition)
        if self.stack:
            for scene in self.stack:
                scene.draw(self.canvas)
        self.tk.after(1, self.tick)

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
