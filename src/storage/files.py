import json
from collections.abc import Mapping
from logging import getLogger
from pathlib import Path
from typing import Any

log = getLogger(__name__)


def load_json(path: Path) -> dict[str, Any] | None:
    try:
        data = json.loads(path.read_bytes())
    except (OSError, ValueError) as error:
        log.warning(f"{path}: f{error}")
        return None
    if not isinstance(data, dict):
        log.warning(f"{path}: expected a JSON object")
        return None
    return data


def save_json(path: Path, data: Mapping[str, object]) -> None:
    try:
        path.write_text(json.dumps(data, indent=2, default=str) + "\n")
    except OSError as error:
        log.error("%s: %s", path, error.strerror)
