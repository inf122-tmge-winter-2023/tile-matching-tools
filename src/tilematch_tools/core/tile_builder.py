"""
    :module_name: tile_builder
    :module_summary: a builder class capable of creating tile classes for a tile-matching game
    :module_author: Nathan Mendoza (nathancm@uci.edu)
"""

from ..model import Tile
from ..model.tile_color import TileColor
from ..model.tile_shape import TileShape

from abc import ABC
from typing import Self

class TileBuilder(ABC):
    """
        A class that allows for construction of different types of tiles
    """

    def __init__(self):
        self._tile_attrs = {}

    def add_position(self, x: int, y: int) -> Self:
        """
            Specify the position of the tile to create
            :arg x: the x value of the tile's position
            :arg y: the y value of the tile's position
            :arg type: int
            :arg type: int
            :returns: updated tile builder
            :rtype: TileBuilder
        """
        self._tile_attrs['position'] = (x, y)
        return self
    
    def add_color(self, color: TileColor):
            """
                Specify the position of the tile to create
                :arg color: color of the tile
                :arg type: str
                :returns: updated tile builder
                :rtype: TileBuilder
            """
            self._tile_attrs['color'] = color
            return self

    def add_shape(self, shape: TileShape):
        """
            Specify the shape of the tile to create
            :arg shape: shape of the tile
            :arg type: str
            :returns: updated tile builder
            :rtype: TileBuilder
        """
        self._tile_attrs['shape'] = shape
        return self

    def construct(self, tile_type = Tile) -> Tile:
        """
            Construct a tile using the tile attrs previously provided
            :arg tile_type: the tile type to construct; defaults to abstract tile
            :arg type: type
            :returns: a new tile_type object
            :rtype: Tile
        """
        return tile_type(**self._tile_attrs)
    
