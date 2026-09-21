from typing import TypeAlias
from pathlib import Path
import base64
import json
from collections import OrderedDict


HighScore: TypeAlias = OrderedDict[str, int]


def load_highscore(filepath: str) -> HighScore:
    path = Path(filepath)
    try:
        encoded_buffer: bytes = path.read_bytes()
        highscore: HighScore = json.loads(
            base64.b64decode(encoded_buffer).decode(),
            object_pairs_hook=OrderedDict
        )
    except (OSError, ValueError):
        save_highscore(OrderedDict(), filepath)
        return OrderedDict()
    return highscore


def update_highscore(
    highscore: HighScore, name: str, score: int, filepath: str
) -> HighScore:
    highscore[name] = score
    highscore.fromkeys
    # sort
    sorted_names: list[str] = sorted(
        highscore, key=lambda k: highscore[k]
    )
    for n in reversed(sorted_names):
        highscore.move_to_end(n)
    # limit length to 10
    for i, k in enumerate(highscore.copy().keys()):
        print(i, k)
        if i >= 10:
            del highscore[n]
    save_highscore(highscore, filepath)
    return highscore


def save_highscore(highscore: HighScore, filepath: str) -> None:
    path = Path(filepath)
    encoded_buffer: bytes = json.dumps(highscore).encode()
    path.write_bytes(base64.b64encode(encoded_buffer))
