"""
    :module_name: tile
    :module_summary: a class that represents the base tile
    :module_author: Matthew Isayan
"""

from abc import ABC
from dataclasses import dataclass

@dataclass
class Position:
    """
        A class that represents a position on a 2d plane
    """
    x: int
    y: int

class Tile(ABC):
    """
        A class the represents a tile in a tile-matching game
    """

    def __init__(self, x, y):
        self._position = Position(x, y)

    @property
    def position(self) -> (int, int):
        """
            Return the position of this tile
            :returns: an snapshot of the tile's current position
            :rtype: Position
        """
        return self._position

    @position.setter
    def position(self, new_pos: (int, int)) -> None:
        """
            Update the position of this tile
            :arg new_pos: a 2-tuple representing the new position coordinate
            :arg type: tuple
            :returns: nothing
            :rtype: None
        """
        self._position.x = new_pos[0]
        self._position.y = new_pos[1]
