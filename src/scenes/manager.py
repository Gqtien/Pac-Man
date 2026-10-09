import time
from render import FrameBuffer
from .base import Scene, Pop, Push, Reset, Transition
from .window import Window


class SceneManager:
    def __init__(self) -> None:
        self.window = Window("PacMan")
        self.framebuffer = FrameBuffer(self.window.width, self.window.height)
        self.stack: list[Scene] = []
        self.keys: set[int] = set()
        self.last = time.perf_counter()

    def start(self, initial_scene: Scene) -> None:
        self.stack.append(initial_scene)
        self.last = time.perf_counter()
        self.window.run(self.tick, self.press)

    @property
    def top(self) -> Scene:
        return self.stack[-1]

    def press(self, keycode: int) -> None:
        self.keys.add(keycode)

    def tick(self) -> None:
        if not self.stack:
            return
        now = time.perf_counter()
        dt, self.last = min(now - self.last, 0.1), now
        keys, self.keys = self.keys, set()
        self.apply(self.top.update(dt, keys))
        if not self.stack:
            self.window.close()
            return
        for scene in self.visible():
            scene.draw(self.framebuffer)
        self.window.show(self.framebuffer)

    def visible(self) -> list[Scene]:
        start = len(self.stack) - 1
        while start > 0 and self.stack[start].transparent:
            start -= 1
        return self.stack[start:]

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
