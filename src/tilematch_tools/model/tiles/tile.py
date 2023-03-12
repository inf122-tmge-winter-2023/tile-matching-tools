"""
    :module_name: tile
    :module_summary: a class that represents the base tile
    :module_author: Matthew Isayan, Nathan Mendoza
"""

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass

from ..exceptions import MissingTilePropertyException, IllegalTileMovementException
from .tile_appearance import TileAppearance, TileShape, TileColor
from .movement_rule import MovementRule

LOGGER = logging.getLogger(__name__)

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
            LOGGER.error('All tiles require a position property')
            raise MissingTilePropertyException(
                    f"{type(self)} requires a `position` property but was not present"
                    )
        self._position = Position(*properties.get('position'))
        self._appearance = TileAppearance(
                    properties.get('color', TileColor.RED),
                    properties.get('shape', TileShape.SQUARE)
                )
        self._movable = True

    def move(self, rule: MovementRule):
        """
            Apply the given movement rule to this tile
            :arg rule: the rule specifying how to modify position
            :arg type: Movement rule
            :returns: nothing
            :rtype: None
        """
        if not self.mobile:
            LOGGER.error('Attempted to move an immovable tile')
            raise IllegalTileMovementException("Can't apply a movement to an inmovable tile")
        self.position = rule.exec(
                self.position.x,
                self.position.y
                )


    def __eq__(self, other):
        """Allows for checking tile equality with =="""
        if not isinstance(other, type(self)):
            LOGGER.debug('Other is not an instance of tile, assuming unequal')
            return False
        return self.color == other.color and self.shape == other.shape

    @property
    def position(self) -> Position:
        """
            Return the position of this tile
            :returns: an snapshot of the tile's current position
            :rtype: Position
        """
        LOGGER.debug('Requested read of position is: %s', str(self._position))
        return self._position

    @property
    def mobile(self) -> bool:
        """
            Returns whether a tile can move
            :returns: tile mobility
            :rtype: bool
        """
        LOGGER.debug('Requested read of mobility is: %s', str(self._movable))
        return self._movable

    @position.setter
    def position(self, new_pos: (int, int)) -> None:
        """
            Update the position of this tile
            :arg new_pos: a 2-tuple representing the new position coordinate
            :arg type: tuple
            :returns: nothing
            :rtype: None
        """
        LOGGER.debug('Updating position: (%d, %d) -> (%d, %d)',
                     self._position.x,
                     self._position.y,
                     new_pos[0],
                     new_pos[1]
                     )
        self._position.x = new_pos[0]
        self._position.y = new_pos[1]

    @property
    def color(self):
        LOGGER.debug('Requested read of tile color is: %s', str(self._appearance.color))
        return self._appearance.color

    @property
    def shape(self):
        LOGGER.debug('Requested read of tile shape is: %s', str(self._appearance.shape))
        return self._appearance.shape

class NullTile(Tile):
    """
        A class that represents the absence of a tile
    """
    def __init__(self, **properties):
        super().__init__(**properties)
        self._movable = False
