from dataclasses import asdict, dataclass, fields
from logging import getLogger
from pathlib import Path
from typing import Any
from .files import load_json, save_json

log = getLogger(__name__)


@dataclass
class Config:
    lives: int = 3
    levels_to_win: int = 3
    speed: float = 10.0
    anim_speed: float = 10.0
    entity_hitbox: float = 0.5
    cheat_win_key: str = "w"
    cheat_invisible_key: str = "i"
    cheat_freeze_ghosts_key: str = "f"
    highscore_filepath: Path = Path("highscore.json")
    spritesheet: Path = Path("assets/spritesheet.png")
    walls: Path = Path("assets/walls.png")
    font: Path = Path("assets/font.png")
    overlay: Path = Path("assets/overlay.png")


def load_config(path: Path) -> Config:
    config = Config()
    data = load_json(path)
    if data is None:
        return config

    missing: bool = False

    for field in fields(config):
        name, default = field.name, getattr(config, field.name)
        if name not in data:
            missing = True
            continue

        value = parse(data[name], default)
        if value is None:
            log.warning(
                f"{path}: invalid {name!r} {data[name]!r}, "
                f"using default {to_json(default)!r}"
            )
            continue

        setattr(config, name, value)

    known = {field.name for field in fields(config)}
    for key in data:
        if key not in known:
            log.warning(f"{path}: unknown key '{key}' ignored")

    if missing:
        defaults = {n: to_json(v) for n, v in asdict(Config()).items()}
        save_json(path, {**defaults, **data})

    return config


def parse(value: Any, default: Any) -> Any:
    if isinstance(value, bool) or isinstance(default, bool):
        return value if type(value) is type(default) else None
    if isinstance(default, Path) and isinstance(value, str):
        return Path(value)
    if isinstance(default, float) and isinstance(value, int):
        value = float(value)
    if not isinstance(value, type(default)):
        return None
    if isinstance(value, (int, float)) and value <= 0:
        return None
    return value


def to_json(value: Any) -> Any:
    if isinstance(value, Path):
        return str(value)
    return value
