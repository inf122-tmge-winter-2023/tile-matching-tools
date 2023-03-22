"""
    :module_name: game_loop
    :module_summary: a class that templates the idea of a game loop
    :module_author: Nathan Mendoza (nathancm@uci.edu)
"""

import logging
import time
from abc import ABC, abstractmethod
from enum import IntEnum

from .game_state import GameState
from .exceptions import GameEndedException
from ..view import GameView
from ..model.match import MatchCondition

LOGGER = logging.getLogger(__name__)

class FPSDelay(IntEnum):
    """Enumeration of delays used of achieve a target FPS in nanoseconds"""
    FPS15 = 66_666_666
    FPS30 = 33_333_333
    FPS60 = 16_666_666
    FPS120 = 8_333_333


class GameLoop(ABC):
    """A class that template a game loop"""

    def __init__(self, state: GameState, view: GameView, delay: FPSDelay = FPSDelay.FPS30):
        self._state = state
        self._view = view
        self._loop_delay = delay
        self._last_call = time.time_ns()

    def __call__(self):
        """Go thru one iteration of the game loop"""
        if self.gameover():
            raise GameEndedException(
                    'The game has already ended. No further loop iterations are allowed'
                    )
        self.await_delay()
        self.handle_input()
        self.update_view()
        while matches := self.find_matches(self._state.match_rules):
            self.clear_matches(matches)
        self.update_view()

    @abstractmethod
    def handle_input(self) -> None:
        """Handle the next input available
            :returns: nothing
            :rtype: None
        """
        pass

    @abstractmethod
    def find_matches(self, match_rules: [MatchCondition]) -> [MatchCondition.MatchFound]:
        """Look for matches that satisfy the given match conditions
            :arg match_rules: list of match conditions to look for
            :arg type: list
            :returns: list of matches found
            :rtype: list
        """
        return []

    @abstractmethod
    def clear_matches(self, matches_found: [MatchCondition.MatchFound]) -> None:
        """Clear the matches found on the board, if any
            :arg matches_found: list of discovered matches to clear
            :arg type: list
            :returns: nothing
            :rtype: None
        """
        for match in matches_found:
            self._state.clear_match(match)
            time.sleep(self._loop_delay)
            self._state.adjust_score(match)

    @abstractmethod
    def update_view(self) -> None:
        """Update the view of the game
            :returns: nothing
            :rtype: None
        """
        self._view.update_game_state(self._state)

    @abstractmethod
    def gameover(self) -> bool:
        """Check if the game has ended
            :returns: true if game over, false otherwise
            :rtype: bool
        """
        return False

    def await_delay(self, delay = None):
        """
            Await the delay necessary to achieve a target FPS
            :returns: nothing
            :rtype: None
        """
        if not delay:
            delay = self._loop_delay
        while time.time_ns() <= self._last_call + delay:
            pass
        self._last_call = time.time_ns()

    @property
    def state(self) -> GameState:
        """
            Return reference to current game state
            :returns: game state snapshot
            :rtype: GameState
        """
        return self._state

    @property
    def view(self) -> GameView:
        """
            Return a reference to current game view
            :returns: game view
            :rtype: GameView
        """
        return self._view
