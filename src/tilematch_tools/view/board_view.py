"""
    :module_name: board_view
    :module_summary: GUI widget for displaying a tilematching game board
    :module_author: Nathan Mendoza (nathancm@uci.edu)
"""

import tkinter as tk
from dataclasses import dataclass

from ..model import GameBoard
from .game_widgets import GameInfo

@dataclass
class BoundingBox:
    start_x: int
    start_y: int
    end_x: int
    end_y: int

class BoardView(GameInfo):
    """GUI widget for displaying a tilematching game board"""
    tile_side_length = 30

    def __init__(self, parent, board_to_watch: GameBoard, **options):
        self._watching = board_to_watch
        super().__init__(parent, **options)

    def update(self):
        for tile in self.watching:
            self._update_tile(tile)
        

    @property
    def watching(self):
        return self._watching

    @property
    def showing(self):
        return self._board_display

    @property
    def board_height(self):
        return self.tile_side_length * self.watching.num_rows

    @property
    def board_width(self):
        return self.tile_side_length * self.watching.num_cols

    @property
    def tiles_map(self):
        if not hasattr(self, '_tiles_map'):
            self._tiles_map = {}

        return self._tiles_map

    def create_widgets(self):
        self._board_display = tk.Canvas(self, width=self.board_width, height=self.board_height)
        self._init_board()

    def place_widgets(self):
        self._board_display.pack(side="left", fill="y")

    def _init_board(self):
        for tile in self.watching:
            self._create_tile(tile)

    def bbox_for_tile(self, tile):
        return BoundingBox(
        start_x = (tile.position.x - 1) * self.tile_side_length,
        start_y = self.board_height - tile.position.y * self.tile_side_length,
        end_x = tile.position.x * self.tile_side_length,
        end_y = self.board_height - (tile.position.y - 1) * self.tile_side_length
        )

    def _create_tile(self, tile):
        bbox = self.bbox_for_tile(tile)
        self.tiles_map[(tile.position.x, tile.position.y)] = self._board_display.create_rectangle(
                bbox.start_x, 
                bbox.start_y, 
                bbox.end_x,
                bbox.end_y, 
                fill=tile.color, 
                outline=tile.border, 
                width=1
            )

    def _update_tile(self, tile):
        bbox = self.bbox_for_tile(tile)
        self._board_display.itemconfig(
                self.tiles_map.get((tile.position.x, tile.position.y)),
                fill=tile.color,
                outline=tile.border,
                width=1
            )
