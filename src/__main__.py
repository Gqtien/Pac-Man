import sys
from scenes import SceneManager
from scenes import Gameplay


def run() -> None:
    SceneManager(Gameplay())


if __name__ == "__main__":
    try:
        run()
    except Exception as exc:
        sys.exit(f"Error: {exc}")
