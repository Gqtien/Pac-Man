from dataclasses import dataclass
import math


@dataclass
class Vec2:
    x: int
    y: int

    def update(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def norm(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __mul__(self, scale: int) -> "Vec2":
        return Vec2(self.x * scale, self.y * scale)

    def __add__(self, other: "Vec2") -> "Vec2":
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vec2") -> "Vec2":
        return Vec2(self.x - other.x, self.y - other.y)
