from abc import ABC, abstractmethod
import time


class Scene(ABC):
    def __init__(self, stack: list["Scene"]) -> None:
        self.stack: list[Scene] = stack

    def enter(self) -> None:
        self.stack.append(self)

    def exit(self) -> None:
        if self in self.stack:
            self.stack.remove(self)

    def switch_to(self, scene: "Scene") -> None:
        self.exit()
        scene.enter()

    @abstractmethod
    def draw(self) -> None: ...

    @abstractmethod
    def update(self, dt: float) -> None: ...


class Gameplay(Scene): ...


class Death(Scene): ...


class Pause(Scene): ...


class Main(Scene): ...


class SceneManager:
    def __init__(self, initial_scene: Scene) -> None:
        self.stack: list[Scene] = [initial_scene]

    def run(self) -> None:
        dt: float = 0.0
        while True:
            if not self.stack:
                return
            scene = self.stack[-1]

            before = time.time()
            scene.update(dt)
            scene.draw()
            dt = time.time() - before
