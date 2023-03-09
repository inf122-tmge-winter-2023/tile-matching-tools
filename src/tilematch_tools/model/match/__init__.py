"""
    :module_name: match
    :module_summary: class that controlls the match rules of a tile-matching game
    :module_author: Nathan Mendoza (nathancm@uci.edu)
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

from ..board import GameBoard
from ..tiles import Tile

class ScanDelta(Enum):
    """
        Enumeration representing the 8 directional unit vectors on a 2d-plan
    """
    UP = (0, 1)
    DOWN = (0, -1)
    RIGHT = (1, 0)
    LEFT = (-1, 0)
    UPANDRIGHT = (1, 1)
    UPANDLEFT = (-1, 1)
    DOWNANDRIGHT = (1, -1)
    DOWNANDLEFT = (-1, -1)

class MatchCondition(ABC):
    """
        Class that specifies the interface for match rules
        :scan: the 2-unit vector direction to scan a match for
        :equality_rule: the function the determines if two tiles match
    """

    @dataclass
    class MatchFound:
        """
            Class representing a discovered match and its point value
        """
        value: int
        matching_tiles: [Tile]

    
    def __init__(self, scan: ScanDelta, value: int, equality_rule: callable = Tile.__eq__):
        self._eq = equality_rule
        self._point_value = value
        self._scan_delta = scan

    @abstractmethod
    def check_match(self, board: GameBoard, start_x: int, start_y: int) -> MatchFound or None:
        """
            Check for a match on the given board starting at the specified position
            :arg board: the board to check a match for
            :arg start_x: the x position the match scan starts at
            :arg start_y: the y position the match scan starts at
            :arg type: GameBoard
            :arg type: int
            :arg type: int
            :returns: A object describing the match if one was found, None otherwise
            :rtype: MatchFound or None
        """
        pass
            
    @property
    def point_value(self) -> int:
        """
            Read only view of the point value of this match condition
            :returns: match condition's point value
            :rtype: int
        """
        return self._point_value
