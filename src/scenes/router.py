from assets import Assets
from storage import Config
from .end import End
from .events import Event, Finish, Init, Leave, Pause, Quit, Resume, Start
from .gameplay import Gameplay
from .main import Main
from .pause import Pause as PauseMenu
from .transition import Clear, Pop, Push, Reset, Transition


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
