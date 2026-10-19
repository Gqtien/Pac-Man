from dataclasses import dataclass
from .base import Scene
from typing import TypeAlias


@dataclass(frozen=True)
class Push:
    scene: Scene


class Pop:
    ...


@dataclass(frozen=True)
class Reset:
    scene: Scene


class Clear:
    ...


Transition: TypeAlias = Push | Pop | Reset | Clear | None
