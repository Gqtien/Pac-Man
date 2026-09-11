from dataclasses import dataclass


@dataclass(frozen=True)
class Push[Scene]:
    scene: Scene


@dataclass(frozen=True)
class Pop:
    ...


@dataclass(frozen=True)
class Reset[Scene]:
    scene: Scene


type Transition[Scene] = Push[Scene] | Pop | Reset[Scene] | None
