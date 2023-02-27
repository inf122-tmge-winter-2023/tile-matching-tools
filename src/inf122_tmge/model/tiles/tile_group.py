"""
    :module_name: tile_group
    :module_summary: a class that allows individual tiles to exists as a group
    :module_author: Nathan Mendoza (nathancm@uci.edu)
"""

from ..exceptions import TileGroupPositionOccupiedError, \
                         TileGroupDisbandedException 

from .tile import Tile, Position

from dataclasses import dataclass


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
            raise TileGroupDisbandedException("Cannot add a sibling Tile to a disbanded TileGroup")
        if self._tiles.get((dx, dy)):
            raise TileGroupPositionOccupiedError(
                    f"Relative position ({dx}, {dy}) is occupied by another tile"
                    )
        new_tile.position = (self._center.position.x + dx, self._center.position.y + dy)
        self._tiles[(dx, dy)] = new_tile

    @property
    def disbanded(self) -> bool:
        """
            Determines if this tile group has disbanded
            :returns: read-only version of disbanded property
            :rtype: bool
        """
        return self._disbanded

    def disband(self) -> None:
        """
            Updates the disbanded property of this tile group to true. Forbids further modification
            :returns: nothing
            :rtype: None
        """
        self._disbanded = True
