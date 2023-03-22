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


class GameLoop(ABC):
    """A class that template a game loop"""

    def __init__(self, state: GameState, view: GameView, delay: int = 1_000_000_000):
        self._state = state
        self._view = view
        self._loop_delay = delay
        self._last_call = time.time_ns()

    def __call__(self):
        """Go thru one iteration of the game loop"""
        if self.state.gameover():
            raise GameEndedException(
                    'The game has already ended. No further loop iterations are allowed'
                    )
        if self.can_advance():
            self.tick()
            while matches := self.find_matches(self._state.match_rules):
                self.clear_matches(matches)
                time.sleep(1)
                self.clean_up_matches()

    @abstractmethod
    def tick(self) -> None:
        """Execute any logic necessary to idly advance the game state
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
    def clean_up_state(self):
        """Clean up the game state after match discovery and removal
            :returns: nothing
            :rtype: None
        """
        pass

   
    def can_advance(self, delay = None) -> bool:
        """
            Guard the loop from excessive calls
            :returns: true if the loop can advance, false otherwise
            :rtype: None
        """
        if not delay:
            delay = self._loop_delay
        if time.time_ns() <= self._last_call + delay:
            return False

        self._last_call = time.time_ns()
        return True

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
