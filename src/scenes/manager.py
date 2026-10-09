import time
from tkinter import Canvas, Event, Tk
from .base import Scene, Pop, Push, Reset, Transition


class SceneManager:
    def __init__(self) -> None:
        self.tk = Tk()
        self.tk.attributes("-zoomed", True)
        self.canvas = Canvas(self.tk, bg="black")
        self.canvas.pack(fill="both", expand=True)
        self.stack: list[Scene] = []
        self.last: float = time.perf_counter()
        self.keys: set[str] = set()
        self.tk.bind("<KeyPress>", self.on_key)
        self.tk.after(0, self.tick)

    def start(self, initial_scene: Scene) -> None:
        self.initial_scene = initial_scene
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
        now = time.perf_counter()
        dt, self.last = min(now - self.last, 0.1), now
        keys, self.keys = self.keys, set()
        self.canvas.delete("all")

        transition: Transition = self.top.update(dt, keys)
        self.apply(transition)
        for scene in self.stack:
            scene.draw(self.canvas)
        spent = time.perf_counter() - now
        self.tk.after(max(1, round((1 / 60 - spent) * 1000)), self.tick)

    def apply(self, transition: Transition) -> None:
        match transition:
            case Push():
                self.stack.append(transition.scene)
            case Pop():
                self.stack.pop()
            case Reset():
                self.stack = [transition.scene]
            case None:
                pass
