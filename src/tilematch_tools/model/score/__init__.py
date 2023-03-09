"""
    :module_name: score
    :module_summary: a class the can represent the score of a tile-matching game
    :module_author: Nathan Mendoza (nathancm@uci.edu)
"""

import logging
from abc import ABC, abstractmethod

from ..match import MatchCondition

LOGGER = logging.getLogger(__name__)

class Scoring(ABC):
    """ a class that tracks the score of a game"""

    def __init__(self):
        self._points = 0
        self._multiplier = 1

    @property
    def score(self) -> int:
        """
            read only view of current score
            :returns: snapshot of score value
            :rtype: int
        """
        LOGGER.debug('Request read of score with value: %d', self._points)
        return self._points

    @property
    def multiplier(self) -> int:
        """
            read only view of score multiplier
            :returns: current score multiplier
            :rtype: int
        """
        LOGGER.debug('Request read of multiplier with value: %d', self._multiplier)
        return self._multiplier

    @multiplier.setter
    def multiplier(self, new_multiplier) -> None:
        """
            write only view of score multiplier
            :arg new_multiplier: the new muliplier value (can be 0)
            :returns: Nothing
            :rtype: None
        """
        LOGGER.debug('Updated multiplier value: %d -> %d', self._multiplier, new_multiplier)
        self._multiplier = new_multiplier

    @abstractmethod
    def award_for_match(self, match: MatchCondition) -> None:
        """
            award the points specified by a given match condition to the score
            :arg match: the match condition awarding points
            :arg type: MatchCondition
            :returns: nothing
            :rtype: None
        """
        LOGGER.warning('Using default implementation. This is meant to be overriden!')
        LOGGER.debug('Adjusting score by %d', self._multiplier * match.point_value)
        self._points += (self._multiplier * match.point_value)
