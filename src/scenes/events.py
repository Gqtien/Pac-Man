from dataclasses import dataclass
from systems import Outcome
from typing import TypeAlias


class Init:
    ...


class Start:
    ...


class Pause:
    ...


class Resume:
    ...


class Leave:
    ...


class Quit:
    ...


@dataclass(frozen=True)
class Finish:
    score: int
    outcome: Outcome


Event: TypeAlias = Init | Start | Pause | Resume | Leave | Quit | Finish | None
