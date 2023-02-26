"""
    :module name: tile_color
    :module_summary: an enumeration of the default tile color shape
    :module_author: Nathan Mendoza (nathancm@uci.edu)
"""


from enum import StrEnum, IntEnum

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


