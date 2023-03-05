"""
    :module_name: tile
    :module_summary: a class that represents the base tile
    :module_author: Matthew Isayan, Nathan Mendoza
"""

from abc import ABC
from dataclasses import dataclass

from ..exceptions import MissingTilePropertyException
from .tile_appearance import TileAppearance
from ..tile_shape import TileShape 
from ..tile_color import TileColor

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

    def __init__(self, **properties):
        if not properties.get('position'):
            raise MissingTilePropertyException(
                    f"{type(self)} requires a `position` property but was not present"
                    )
        self._position = Position(*properties.get('position'))
        self._appearance = TileAppearance(
                    properties.get('color', TileColor.RED),
                    properties.get('shape', TileShape.SQUARE)
                )

    def __eq__(self, other: Tile):
        """Allows for checking tile equality with =="""
        if not isinstance(Tile, other):
            return False
        return self.color == other.color and self.shape == other.shape

    @property
    def position(self) -> Position:
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

    @property
    def color(self):
        return self._appearance.color

    @property
    def shape(self):
        return self._appearance.shape
