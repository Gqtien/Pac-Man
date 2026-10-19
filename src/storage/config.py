from dataclasses import Field, asdict, dataclass, field, fields
from logging import getLogger
from pathlib import Path
from typing import Any
from models import Keys
from .files import load_json, save_json

log = getLogger(__name__)


@dataclass
class Config:
    lives: int = field(default=3, metadata={"bounds": (1, 99)})
    levels_to_win: int = field(default=3, metadata={"bounds": (1, 99)})
    level_time_limit: int = field(default=180, metadata={"bounds": (1, 3600)})
    speed: float = field(default=10.0, metadata={"bounds": (1, 15)})
    entity_hitbox: float = field(default=0.5, metadata={"bounds": (0.25, 1)})
    cheat_win_key: Keys = Keys.W
    cheat_invincible_key: Keys = Keys.I
    cheat_freeze_ghosts_key: Keys = Keys.F
    highscore_path: Path = Path("saves/highscore.json")


def load_config(path: Path) -> Config:
    config = Config()
    data = load_json(path)
    if data is not None:
        fill(config, data, path)
    config.highscore_path = path.parent / config.highscore_path
    return config


def fill(config: Config, data: dict[str, Any], path: Path) -> None:
    missing: bool = False

    for entry in fields(config):
        name, default = entry.name, getattr(config, entry.name)
        if name not in data:
            missing = True
            continue

        value = parse(entry, data[name], default)
        if value is None:
            log.warning(
                f"{path}: invalid {name!r} {data[name]!r}, "
                f"using default {to_json(default)!r}"
            )
            continue

        setattr(config, name, value)

    known = {entry.name for entry in fields(config)}
    for key in data:
        if key not in known:
            log.warning(f"{path}: unknown key '{key}' ignored")

    if missing:
        defaults = {n: to_json(v) for n, v in asdict(Config()).items()}
        save_json(path, {**defaults, **data})


def parse(entry: Field, value: Any, default: Any) -> Any:
    if isinstance(value, bool) or isinstance(default, bool):
        return value if type(value) is type(default) else None
    if isinstance(default, Keys):
        return {k.name.lower(): k for k in Keys if len(k.name) == 1}.get(
            value.lower()
        ) if isinstance(value, str) else None
    if isinstance(default, Path):
        return Path(value) if isinstance(value, str) else None
    if not isinstance(value, (int, float)):
        return None
    if isinstance(default, int) and isinstance(value, float):
        return None
    low, high = entry.metadata["bounds"]
    return type(default)(value) if low <= value <= high else None


def to_json(value: Any) -> Any:
    if isinstance(value, Keys):
        return value.name.lower()
    if isinstance(value, Path):
        return str(value)
    return value
