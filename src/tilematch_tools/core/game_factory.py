from abc import ABC, abstractmethod
import logging

from .game_state import GameState
from .game_loop import GameLoop
from ..view import GameView

LOGGER = logging.getLogger(__name__)

class Game(ABC):
    state: GameState #Should be an instance
    loop: GameLoop #Should be a class to create
    view: GameView #Should be a class to create
    tick_speed: int

    @abstractmethod
    def setup():
        """
            Initial setup of a game and will be called after creation.
        """
        LOGGER.warning('Using default implementation in setup(). This is meant to be overridden!')
        pass
            

class GameFactory(ABC):
    """
        Responsible for creating a game ready to run.
    """
    @abstractmethod
    def create_game(state: GameState, loop : GameLoop, view: GameView, tick_speed: int):
        game =  Game(state, loop, view, tick_speed)
        game.setup()
        return game
