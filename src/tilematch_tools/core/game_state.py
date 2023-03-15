"""
    :module_name: game_state
    :module_summary: an extensible class capable of representing the state of a tile-matching game
    :module_author: Nathan Mendoza (nathancm@uci.edu), Matthew Isayan
"""

import logging

from ..model import GameBoard, Scoring, MatchCondition

LOGGER = logging.getLogger(__name__)

class GameState:
    """
        Class responsible for holding the gameboard and score 
    """
    def __init__(self, board: GameBoard, score: Scoring):
        self._board = board
        self._score = score
        self._match_conditions = []



    def add_match_condition(self, match_cond):
        """
            Adds a match conditions that can affect this game state
            :arg match_cond: the new match condition
            :arg type: MatchCondition
            :returns: nothing
            :rtype: None
        """
        self._match_conditions.append(match_cond)

    @property
    def match_rules(self):
        return self._match_conditions
