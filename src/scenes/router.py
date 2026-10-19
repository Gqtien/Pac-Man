from storage import Config
from assets import Assets
from .events import Event, Init, Start, Pause, Resume, Finish, Leave, Quit
from .transition import Transition, Push, Pop, Reset, Clear
from .gameplay import Gameplay
from .pause import Pause as PauseMenu
from .end import End
from .main import Main


class Router:
    def __init__(self, config: Config, assets: Assets) -> None:
        self.config = config
        self.assets = assets

    def route(self, event: Event) -> Transition:
        match event:
            case Init() | Leave():
                return Reset(Main(self.config, self.assets))
            case Start():
                return Push(Gameplay(self.config, self.assets))
            case Pause():
                return Push(PauseMenu(self.assets))
            case Resume():
                return Pop()
            case Finish(score, outcome):
                return Reset(End(self.config, self.assets, score, outcome))
            case Quit():
                return Clear()
        return None
