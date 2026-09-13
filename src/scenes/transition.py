from dataclasses import dataclass
from typing import Generic, TypeAlias, TypeVar

Scene = TypeVar("Scene")


@dataclass(frozen=True)
class Push(Generic[Scene]):
    scene: Scene


@dataclass(frozen=True)
class Pop:
    ...


@dataclass(frozen=True)
class Reset(Generic[Scene]):
    scene: Scene


Transition: TypeAlias = Push[Scene] | Pop | Reset[Scene] | None
