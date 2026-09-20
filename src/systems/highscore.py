from pathlib import Path
import json

def load_highscore(filepath: str) -> int:
    path = Path(filepath)
    if not path.exists():
        save_highscore(0, filepath)
    highscore: int = json.loads(path.read_text())
    return highscore


def save_highscore(highscore: int, filepath: str) -> None:
    path = Path(filepath)
    path.write_text(json.dumps(highscore))
