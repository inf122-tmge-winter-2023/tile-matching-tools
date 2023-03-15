"""
    :module_name: game_loop
    :module_summary: a class that templates the idea of a game loop
    :module_author: Nathan Mendoza (nathancm@uci.edu)
"""

import logging
import time
import tkinter as tk
from abc import ABC, abstractmethod
from enum import IntEnum

from .game_state import GameState
from ..view import View
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

    def __init__(self, state: GameState, view: View, delay: FPSDelay = FPSDelay.FPS30):
        self._state = state
        self._view = view
        self._loop_delay = delay
        self._last_call = time.time_ns()

    def __call__(self):
        """Go thru one iteration of the game loop"""
        self.await_delay()
        self.handle_input()
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
        pass

    @abstractmethod
    def update_view(self) -> None:
        """Update the view of the game
            :returns: nothing
            :rtype: None
        """
        pass

    def await_delay(self):
        """
            Await the delay necessary to achieve a target FPS
            :returns: nothing
            :rtype: None
        """
        while time.time_ns() <= self._last_call + self._loop_delay:
            pass
        self._last_call = time.time_ns()
