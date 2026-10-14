import os
import json
from collections.abc import Mapping
from logging import getLogger
from pathlib import Path
from typing import Any

log = getLogger(__name__)


def load_json(path: Path) -> dict[str, Any] | None:
    if not os.path.isfile(path):
        log.warning(f"{path}: missing or not a regular file")
        return None
    try:
        data = json.loads(path.read_bytes())
    except (OSError, ValueError, RecursionError) as error:
        log.warning(f"{path}: {error}")
        return None
    if not isinstance(data, dict):
        log.warning(f"{path}: expected a JSON object")
        return None
    return data


def save_json(path: Path, data: Mapping[str, object]) -> None:
    if os.path.exists(path) and not os.path.isfile(path):
        log.error(f"{path}: not a regular file")
        return
    try:
        path.write_text(json.dumps(data, indent=2, default=str) + "\n")
    except (OSError, ValueError) as error:
        log.error(f"{path}: {error}")
