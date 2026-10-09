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
        save_config(path, config)
        return config
    if not isinstance(data, dict):
        log.warning(f"{path}: expected an object, using default config")
        save_config(path, config)
        return config

    needs_save: bool = False

    for field in fields(config):
        name, default = field.name, field.default
        if name not in data:
            needs_save = True
            continue

        value = data.pop(name)

        if not same_type(value, default):
            log.warning(
                f"{path}: {name!r} must be a {type(default).__name__}, "
                f"got {type(value).__name__}, using default {default}"
            )
            needs_save = True
            continue

        if isinstance(default, float) and isinstance(value, int):
            value = float(value)

        setattr(config, name, value)

    for key in data:
        log.warning(f"{path}: unknown key '{key}' ignored and will be removed")
        needs_save = True

    if needs_save:
        save_config(path, config)

    return config


def save_config(path: Path, config: Config) -> None:
    try:
        config_dict = asdict(config)
        path.write_text(json.dumps(config_dict, indent=2) + "\n")
    except OSError as e:
        log.error(f"Failed to write config to {path}: {e}")


def same_type(value: Any, default: Any) -> bool:
    if isinstance(value, bool) or isinstance(default, bool):
        return type(value) is type(default)
    if isinstance(default, float):
        return isinstance(value, (int, float))
    return isinstance(value, type(default))
