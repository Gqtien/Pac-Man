from abc import ABC, abstractmethod
from tkinter import Canvas
from models import Transition


class Scene(ABC):
    @abstractmethod
    def update(self, dt: float, keys: set[str]) -> Transition: ...

    @abstractmethod
    def draw(self, canvas: Canvas) -> None: ...
