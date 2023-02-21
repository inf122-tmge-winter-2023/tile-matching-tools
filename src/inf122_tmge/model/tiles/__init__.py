"""
    :module_name: tiles
    :module_summary: a collection of classes that represent tiles in a tile-matching game
    :module_author: Nathan Mendoza (nathancm@uci.edu)
"""

from abc import ABC

from .tile_shape import TileShape
from .tile_appearance import TileAppearance
from .movement_rule import MovementRule

class Tile(ABC):
    pass
