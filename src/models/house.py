from .entity import GhostPersonality


DOT_LIMITS: dict[int, dict[GhostPersonality, int]] = {
    1: {
        GhostPersonality.BLINKY: 0,
        GhostPersonality.PINKY: 0,
        GhostPersonality.INKY: 30,
        GhostPersonality.CLYDE: 60,
    },
    2: {
        GhostPersonality.BLINKY: 0,
        GhostPersonality.PINKY: 0,
        GhostPersonality.INKY: 0,
        GhostPersonality.CLYDE: 50,
    },
    3: {
        GhostPersonality.BLINKY: 0,
        GhostPersonality.PINKY: 0,
        GhostPersonality.INKY: 0,
        GhostPersonality.CLYDE: 0,
    },
}

STARVE_LIMITS: dict[int, float] = {1: 4.0, 5: 3.0}


def dot_limit(level: int, personality: GhostPersonality) -> int:
    return DOT_LIMITS[max(s for s in DOT_LIMITS if s <= level)][personality]


def starve_limit(level: int) -> float:
    return STARVE_LIMITS[max(s for s in STARVE_LIMITS if s <= level)]
