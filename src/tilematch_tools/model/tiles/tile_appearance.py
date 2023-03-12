"""
    :module_name: tile_appearance
    :module_summary: a class the dictates the appearance of a tile
    :module_author: Nathan Mendoza (nathancm@uci.edu)
"""

from abc import ABC
from dataclasses import dataclass
from enum import StrEnum, IntEnum

class TileShape(IntEnum):
    SQUARE = 1
    DIAMOND = 2
    CIRCULAR = 3

class TileColor(StrEnum):
    """
        Class the enumerates possible default set of colors for tile appearance
    """
    RED = '#FF0000'
    ORANGE = '#FF7F00'
    YELLOW = '#FFFF00'
    GREEN = '#00FF00'
    BLUE = '#0000FF'
    INDIGO = '#4B0082'
    VIOLET = '#9400D3'

@dataclass
class TileAppearance(ABC):
    """
        Class that stores appearance information of a tile
    """
    color: TileColor
    shape: TileShape
