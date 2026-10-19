from abc import ABC, abstractmethod
from render import FrameBuffer
from .events import Event


class Scene(ABC):
    transparent: bool = False

    @abstractmethod
    def update(self, dt: float, keys: set[int]) -> Event: ...

    @abstractmethod
    def draw(self, framebuffer: FrameBuffer) -> None: ...
