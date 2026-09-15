import json
from logging import getLogger, Logger
from dataclasses import fields
from pathlib import Path
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

    for field in fields(config):
        if field.name not in data:
            continue
        value = data.pop(field.name)
        default = getattr(config, field.name)
        if not same_type(value, default):
            log.warning(
                f"{path}: {field.name} must be a {type(default).__name__}, "
                f"got {value}, using default {default}",
            )
            continue
        if isinstance(default, float):
            value = float(value)
        setattr(config, field.name, value)
    for key in data:
        log.warning(f"{path}: unknown key {key} ignored")
    return config


def same_type(value: object, default: object) -> bool:
    if isinstance(value, bool) or isinstance(default, bool):
        return type(value) is type(default)
    if isinstance(default, float):
        return isinstance(value, (int, float))
    return isinstance(value, type(default))
