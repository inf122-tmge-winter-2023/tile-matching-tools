"""
    :module_name: tiles
    :module_summary: a collection of classes that represent tiles in a tile-matching game
    :module_author: Nathan Mendoza (nathancm@uci.edu)
"""

from .tile_appearance import TileAppearance, TileShape, TileColor
from .movement_rule import MovementRule
from .tile import Tile, NullTile
from .tile_group import TileGroup
