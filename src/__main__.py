import sys
from scenes import SceneManager


def run() -> None:
    SceneManager()


if __name__ == "__main__":
    try:
        run()
    except Exception as exc:
        sys.exit(f"Error: {exc}")
