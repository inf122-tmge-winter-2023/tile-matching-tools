"""
    :module_name: tile_shape
    :module_summary: a class that dictates the shape of a given tile
    :module_author: Nathan Mendoza (nathancm@uci.edu)
"""

from enum import IntEnum

class TileShape(IntEnum):
    SQUARE = 1
    DIAMOND = 2
    CIRCULAR = 3
