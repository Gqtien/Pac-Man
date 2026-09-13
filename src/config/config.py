from dataclasses import dataclass


@dataclass
class Config:
    speed: float = 3.0
    spritesheet: str = "assets/spritesheet.png"
    font: str = "assets/font.png"
