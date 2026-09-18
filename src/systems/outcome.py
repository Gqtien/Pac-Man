from enum import Enum, auto


class Outcome(Enum):
    WON = auto()
    DIED = auto()
    LOST = auto()
    CONTINUE = auto()
