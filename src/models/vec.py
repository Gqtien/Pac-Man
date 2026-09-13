from dataclasses import dataclass


@dataclass
class Vec2:
    x: int
    y: int

    def update(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
