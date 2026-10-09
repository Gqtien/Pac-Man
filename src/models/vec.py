import math
from collections.abc import Iterator
from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class Vec2:
    x: int
    y: int

    def __add__(self, other: "Vec2") -> "Vec2":
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vec2") -> "Vec2":
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, scale: int) -> "Vec2":
        return Vec2(self.x * scale, self.y * scale)

    def __iter__(self) -> Iterator[int]:
        yield self.x
        yield self.y

    def norm(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)
