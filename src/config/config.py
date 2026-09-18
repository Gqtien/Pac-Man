from dataclasses import dataclass


@dataclass
class Config:
    speed: float = 3.0
    anim_speed: float = 10.0
    entity_hitbox: float = 0.5
    spritesheet: str = "assets/spritesheet.png"
    walls: str = "assets/walls.png"
    font: str = "assets/font.png"
    overlay: str = "assets/overlay.png"
