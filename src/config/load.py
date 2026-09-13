import json
import logging
from dataclasses import fields
from pathlib import Path
from .config import Config

log = logging.getLogger(__name__)


def load_config(path: Path) -> Config:
    config = Config()
    try:
        data = json.loads(path.read_text())
    except (OSError, ValueError) as e:
        log.warning("%s: %s, using default config", path, e)
        return config
    if not isinstance(data, dict):
        log.warning("%s: expected an object, using default config", path)
        return config

    for field in fields(config):
        if field.name not in data:
            continue
        value = data.pop(field.name)
        default = getattr(config, field.name)
        if not same_type(value, default):
            log.warning(
                "%s: %s must be a %s, got %r, using default %r",
                path, field.name, type(default).__name__, value, default
            )
            continue
        if isinstance(default, float):
            value = float(value)
        setattr(config, field.name, value)
    for key in data:
        log.warning("%s: unknown key %r ignored", path, key)
    return config


def same_type(value: object, default: object) -> bool:
    if isinstance(value, bool) or isinstance(default, bool):
        return type(value) is type(default)
    if isinstance(default, float):
        return isinstance(value, (int, float))
    return isinstance(value, type(default))
