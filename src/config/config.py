from dataclasses import dataclass


@dataclass
class Config:
    speed: float = 3.0
    anim_speed: float = 3.0
    spritesheet: str = "assets/spritesheet.png"
    walls: str = "assets/walls.png"
    font: str = "assets/font.png"
    overlay: str = "assets/overlay.png"
