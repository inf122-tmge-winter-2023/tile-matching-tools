"""
    :module_name: tile_group
    :module_summary: a class that allows individual tiles to exists as a group
    :module_author: Nathan Mendoza (nathancm@uci.edu)
"""

import logging
from dataclasses import dataclass

from .tile import Tile, Position
from ..exceptions import TileGroupDisbandedException, TileGroupPositionOccupiedError

LOGGER = logging.getLogger(__name__)

class TileGroup:
    """
        A class that allows individual tiles to exist as a group
    """

    def __init__(self, center_tile: Tile):
        self._center = center_tile
        self._disbanded = False
        self._tiles = {
                (0, 0): self._center
                }

    def add_sibling_tile(self, new_tile: Tile, dx: int, dy: int) -> None:
        """
            Adds a sibling tile to the group. Relative position will be forced upon the new tile
            :arg new_tile: the new sibling tile
            :arg dx: horizontal positioning relative to the center tile
            :arg dy: vertical positioning relative to the center tile
            :arg type: Tile
            :arg type: int
            :arg type: int
            :returns: nothing
            :rtype: None
            :raises: TileGroupPositionOccupiedError if the relative positioning already has a tile    
            :raises: TileGroupDisbandedException if this tile group has disbanded
        """
        if self.disbanded:
            LOGGER.error('Attempted to add a sibling to a disbanded group')
            raise TileGroupDisbandedException("Cannot add a sibling Tile to a disbanded TileGroup")
        if self._tiles.get((dx, dy)):
            LOGGER.error('Attempted to add a sibling to a relative position that is already occupied')
            raise TileGroupPositionOccupiedError(
                    f"Relative position ({dx}, {dy}) is occupied by another tile"
                    )
        LOGGER.info('Adding sibling tile (%d, %d) offset from center', dx, dy)
        new_tile.position = (self._center.position.x + dx, self._center.position.y + dy)
        self._tiles[(dx, dy)] = new_tile

    """Deprecated
    def move(self, rule: MovementRule) -> None:
    
            Apply the given rule to the tile group by applying the rule to each tile in the group
            :arg rule: the object describing the movement
            :returns: nothing
            :rtype: None
        
        LOGGER.info('Applying a movement rule to a tile group')
        for tile in self._tiles.values():
            tile.move(rule)
    """

    @property
    def disbanded(self) -> bool:
        """
            Determines if this tile group has disbanded
            :returns: read-only version of disbanded property
            :rtype: bool
        """
        LOGGER.debug('Requested read of disbanded property is: %s', str(self._disbanded))
        return self._disbanded

    @property
    def size(self) -> int:
        """
            Returns the number of tiles in this group
            :returns: the tile count
            :rtype: int
        """
        LOGGER.debug('Requested read of size property is: %d', len(self._tiles))
        return len(self._tiles)

    def disband(self) -> None:
        """
            Updates the disbanded property of this tile group to true. Forbids further modification
            :returns: nothing
            :rtype: None
        """
        LOGGER.info('Marking this tile group as disbanded. Mutator operations are now disallowed')
        self._disbanded = True
