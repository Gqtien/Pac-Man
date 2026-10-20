from dataclasses import dataclass
from typing import TypeAlias
from .base import Scene


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
