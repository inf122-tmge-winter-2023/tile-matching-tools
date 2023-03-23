from abc import ABC, abstractmethod
import logging
from typing import Type

from .game_state import GameState
from .game_loop import GameLoop
from ..view import GameView

LOGGER = logging.getLogger(__name__)

class Game(ABC):
    def __init__(self, state: GameState, loop_class: Type[GameLoop], view_class: Type[GameView], tick_speed: int):
        self.state = state
        self.loop = loop_class
        self.view = view_class
        self.tick_speed = tick_speed

    def setup():
        """
            Initial setup of a game and should be called after creation.
        """
        LOGGER.warning('Using default implementation in setup(). This is meant to be overridden!')
            

class GameFactory(ABC):
    """
        Responsible for creating a game ready to run.
    """
    @staticmethod
    @abstractmethod
    def create_game() -> Game:
        """Creates a packaged game that's ready to execute

        Args:
            board_height (int): number of rows on the board
            board_width (int):  number of cols on the board
            tick_speed (int): time in nanoseconds between each update

        Returns:
            Game:  Initialized game that's ready to execute
        """
        LOGGER.warning('Using default implementation in create_game(). This is meant to be overridden!')
