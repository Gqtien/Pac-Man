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
    cheat_win_key: str = "w"
    cheat_invisible_key: str = "i"
    cheat_freeze_ghosts_key: str = "f"
    levels_to_win: int = 3
    highscore_filepath: str = "highscore.json"
    # lives: int = 3
    # points_per_pacgum: int = 10
    # points_per_super_pacgum: int = 50
    # points_per_ghost: int = 200
