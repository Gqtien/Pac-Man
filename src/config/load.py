import json
from dataclasses import fields, asdict
from logging import getLogger, Logger
from pathlib import Path
from typing import Any
from .config import Config

log: Logger = getLogger(__name__)


def load_config(path: Path) -> Config:
    config = Config()

    try:
        data = json.loads(path.read_text())
    except (OSError, ValueError) as e:
        log.warning(f"{path}: {e}, using default config")
        return config
    if not isinstance(data, dict):
        log.warning(f"{path}: expected an object, using default config")
        return config

    missing: bool = False

    for field in fields(config):
        name, default = field.name, field.default
        if name not in data:
            missing = True
            continue

        value = data[name]

        if not same_type(value, default):
            log.warning(
                f"{path}: {name!r} must be a {type(default).__name__}, "
                f"got {type(value).__name__}, using default {default}"
            )
            continue

        if isinstance(default, float) and isinstance(value, int):
            value = float(value)

        setattr(config, name, value)

    known = {field.name for field in fields(config)}
    for key in data:
        if key not in known:
            log.warning(f"{path}: unknown key '{key}' ignored")

    if missing:
        save_config(path, {**asdict(Config()), **data})

    return config


def save_config(path: Path, data: dict[str, Any]) -> None:
    try:
        path.write_text(json.dumps(data, indent=2) + "\n")
    except OSError as e:
        log.error(f"Failed to write config to {path}: {e}")


def same_type(value: Any, default: Any) -> bool:
    if isinstance(value, bool) or isinstance(default, bool):
        return type(value) is type(default)
    if isinstance(default, float):
        return isinstance(value, (int, float))
    return isinstance(value, type(default))
