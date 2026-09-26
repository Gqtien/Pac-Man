from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from models import FrameBuffer
from typing import TypeAlias


class Scene(ABC):
    @abstractmethod
    def update(self, dt: float, keys: set[str]) -> Transition: ...

    @abstractmethod
    def draw(self, framebuffer: FrameBuffer) -> None: ...


@dataclass(frozen=True)
class Push():
    scene: Scene


@dataclass(frozen=True)
class Pop:
    ...


@dataclass(frozen=True)
class Reset():
    scene: Scene


Transition: TypeAlias = Push | Pop | Reset | None
