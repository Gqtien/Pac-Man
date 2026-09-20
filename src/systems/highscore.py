from pathlib import Path
import base64

def load_highscore(filepath: str) -> int:
    path = Path(filepath)
    if not path.exists():
        save_highscore(0, filepath)
    try:
        encoded_buffer: bytes = path.read_bytes()
        highscore: int = int(base64.b64decode(encoded_buffer).decode())
    except (OSError, ValueError):
        save_highscore(0, filepath)
        return 0
    return highscore


def save_highscore(highscore: int, filepath: str) -> None:
    path = Path(filepath)
    encoded_buffer: bytes = str(highscore).encode()
    path.write_bytes(base64.b64encode(encoded_buffer))
