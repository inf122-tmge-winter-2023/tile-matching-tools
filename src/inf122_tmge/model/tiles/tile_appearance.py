"""
    :module_name: tile_appearance
    :module_summary: a class the dictates the appearance of a tile
    :module_author: Nathan Mendoza (nathancm@uci.edu)
"""

from abc import ABC
from dataclasses import dataclass

from ..tile_color import TileColor
from ..tile_shape import TileShape

@dataclass
class TileAppearance(ABC):
    """
        Class that stores appearance information of a tile
    """
    color: TileColor
    shape: TileShape
