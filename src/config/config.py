from dataclasses import dataclass


@dataclass
class Config:
    lives: int = 3
    levels_to_win: int = 3
    speed: float = 3.0
    anim_speed: float = 10.0
    entity_hitbox: float = 0.5
    cheat_win_key: str = "w"
    cheat_invisible_key: str = "i"
    cheat_freeze_ghosts_key: str = "f"
    highscore_filepath: str = "highscore.json"
    spritesheet: str = "assets/spritesheet.png"
    walls: str = "assets/walls.png"
    font: str = "assets/font.png"
    overlay: str = "assets/overlay.png"
