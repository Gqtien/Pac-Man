from dataclasses import dataclass


@dataclass(frozen=True)
class Speed:
    default: float
    fright: float


@dataclass(frozen=True)
class Speeds:
    pacman: Speed
    ghost: Speed


SPEEDS: dict[int, Speeds] = {
    1: Speeds(Speed(0.8, 0.9), Speed(0.75, 0.5)),
    2: Speeds(Speed(0.9, 0.95), Speed(0.85, 0.55)),
    5: Speeds(Speed(1.0, 1.0), Speed(0.95, 0.6)),
    21: Speeds(Speed(0.9, 0.9), Speed(0.95, 0.95)),
}


def speeds(level: int) -> Speeds:
    return SPEEDS[max(start for start in SPEEDS if start <= level)]
