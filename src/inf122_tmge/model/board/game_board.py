"""
    :module_name: game_board
    :module_summary: a classe that represents the board of a tile-matching game
    :module_author: Nathan Mendoza (nathancm@uci.edu)
"""

from abc import ABC

from ..tiles.tile import Tile

class GameBoard(ABC):
    def __init__(self,width, height):
        self._width = width
        self._height = height
        self.__init_board(width, height)

    @property
    def board(self):
        return self._board

    @property
    def width(self):
        return self._width
    
    @property
    def height(self):
        return self._height

    def __init_board(self, width, height):
        self._board = []
        # Fancy Python one liner
        # self._board = [[Tile() for j in range(height)] for i in range(width)]
        for _ in range(width):
            row = []
            for _ in range(height):
                row.append(Tile())
            self._board.append(row)
    
    def update_tile(self, row, col, tile):
        self.board[row][col] = tile
