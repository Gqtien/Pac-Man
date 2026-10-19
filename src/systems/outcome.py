from enum import Enum, auto


class Outcome(Enum):
    WON = auto()
    LOST = auto()
    TIMED_OUT = auto()
