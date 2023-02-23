"""
    :module_name: tile
    :module_summary: a class that represents the base tile
    :module_author: Matthew Isayan
"""

from abc import ABC

class Tile(ABC):
    def __init__(self, color='#D3D3D3'):
        self.color = color
