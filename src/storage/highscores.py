import os
from logging import getLogger
from pathlib import Path
from typing import Any, TypeAlias, Iterable
from .files import load_json, save_json

log = getLogger(__name__)


Highscores: TypeAlias = dict[str, int]


def load_highscores(path: Path) -> Highscores:
    if not os.path.isfile(path):
        return {}
    data = load_json(path)
    if data is None:
        return {}
    scores = {
        name: score
        for name, score in data.items()
        if is_entry(name, score)
    }
    if ignored := len(data) - len(scores):
        log.warning(f"{path}: {ignored} invalid scores ignored")
    return ranked(scores.items())


def is_entry(name: str, score: Any) -> bool:
    return (
        0 < len(name) <= 10
        and type(score) is int
        and 0 <= score <= 9_999_999
    )


def save_score(path: Path, name: str, score: int) -> None:
    if not can_overwrite(path):
        log.error(f"{path}: not a highscore file, score not saved")
        return
    scores = with_score(load_highscores(path), name, score)
    save_json(path, scores)


def can_overwrite(path: Path) -> bool:
    if not os.path.exists(path):
        return True
    data = load_json(path)
    return data is not None and all(type(s) is int for s in data.values())


def with_score(scores: Highscores, name: str, score: int) -> Highscores:
    if name in scores and scores[name] > score:
        return scores
    others = [entry for entry in scores.items() if entry[0] != name]
    return ranked([(name, score), *others])


def ranked(entries: Iterable[tuple[str, int]]) -> Highscores:
    best = sorted(entries, key=lambda entry: entry[1], reverse=True)
    return dict(best[:10])
