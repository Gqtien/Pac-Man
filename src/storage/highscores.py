from collections.abc import Iterable
from logging import getLogger
from pathlib import Path
from typing import TypeAlias
from .files import load_json, save_json

log = getLogger(__name__)


Highscores: TypeAlias = dict[str, int]


def load_highscores(path: Path) -> Highscores:
    if not path.exists():
        return {}
    data = load_json(path)
    if data is None:
        return {}
    scores = {
        name: score
        for name, score in data.items()
        if type(score) is int and score >= 0
    }
    if ignored := len(data) - len(scores):
        log.warning(f"{path}: f{ignored} invalid scores ignored")
    return ranked(scores.items())


def save_score(path: Path, name: str, score: int) -> None:
    scores = with_score(load_highscores(path), name, score)
    save_json(path, scores)


def with_score(scores: Highscores, name: str, score: int) -> Highscores:
    if name in scores and scores[name] > score:
        return scores
    others = [entry for entry in scores.items() if entry[0] != name]
    return ranked([(name, score), *others])


def ranked(entries: Iterable[tuple[str, int]]) -> Highscores:
    best = sorted(entries, key=lambda entry: entry[1], reverse=True)
    return dict(best[:10])
