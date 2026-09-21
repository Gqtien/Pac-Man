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
    highscore.move_to_end(name, last=False)
    keys = list(highscore.keys())
    # shift new entry to the right until it's sorted
    for k in reversed(keys[1:]):
        if highscore[k] > highscore[name]:
            highscore.move_to_end(k, last=False)
    # if more than ten, remove last elements
    for i, k in enumerate(highscore.copy()):
        if i >= 10:
            del highscore[k]
    save_highscore(highscore, filepath)
    return highscore


def save_highscore(highscore: HighScore, filepath: str) -> None:
    path = Path(filepath)
    encoded_buffer: bytes = json.dumps(highscore).encode()
    path.write_bytes(base64.b64encode(encoded_buffer))
