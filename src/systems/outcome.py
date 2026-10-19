from enum import Enum, auto
from typing import Literal, TypeAlias


class Outcome(Enum):
    WON = auto()
    DIED = auto()
    LOST = auto()
    TIMED_OUT = auto()
    CONTINUE = auto()


Ending: TypeAlias = Literal[Outcome.WON, Outcome.LOST, Outcome.TIMED_OUT]
