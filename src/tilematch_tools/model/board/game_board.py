"""
    :module_name: game_board
    :module_summary: a classe that represents the board of a tile-matching game
    :module_author: Nathan Mendoza (nathancm@uci.edu)
"""

from abc import ABC

from ..tiles import Tile, MovementRule
from ..exceptions import InvalidBoardPositionError, IllegalBoardContentException

class GameBoard(ABC):
    def __init__(self,width, height):
        self._num_rows = height
        self._num_cols = width
        self.__init_board()

    @property
    def board(self):
        return self._board
        
    @property
    def num_rows(self):
        return self._num_rows

    @property
    def num_cols(self):
        return self._num_cols

    def __init_board(self) -> None:
        """
            initialize the game board full of default tiles
            :returns: nothing
            :rtype: None
        """
        self._board = [ # positions will be represented as positve cartesian coordinates
                [ Tile(**{'position': (x, y),'color':'#D3D3D3'}) for y in range(1, self._num_rows + 1)]
                for x in range(1, self._num_cols + 1)
                ]

    def tile_at(self, x: int, y: int) -> Tile:
        """
           return a reference to the tile at the specified location on the game board
           :arg x: the x value of the coordinate to obtain the tile from
           :arg y: the y value of the coordinate to obtain the tile from
           :returns: a reference to the specified tile
           :rtype: Tile
           :throws: InvalidBoardPositionError if the specified position is invalid
        """
        if not self.__board_position_is_valid(x, y):
            raise InvalidBoardPositionError(
                f"The position ({x}, {y}) is invalid for the given board"
                    )
        return self._board[x - 1][y - 1] # Adjust from cartesian coordinates to valid indices

    def place_tile(self, tile: Tile, x: int, y: int) -> None:
        """
            place the given tile at the specified location forcefully
            :arg tile: tile to place
            :arg x: the x value of the location
            :arg y: the y value of the location
            :arg type: Tile
            :arg type: int
            :arg type: int
            :returns: nothing
            :rtype: None
            :throws InvalidBoardPositionError if the specified position is invalid
            :throws IllegalBoardContentException if the given tile is not a Tile
        """
        if not self.__board_position_is_valid(x, y):
            raise InvalidBoardPositionError(
                    f"The position ({x}, {y}) is invalid for the given board"
                    )
        if not isinstance(tile, Tile):
            raise IllegalBoardContentException(
                    f"tile must be of type Tile, not {type(tile)}"
                    )
        self._board[x - 1][y - 1] = tile
        tile.position = (x, y)
            

    def __board_position_is_valid(self, x: int, y: int):
        """
            Returns true if the given (x, y) ordered pair is valid on this board. False otherwise
            :arg x: the x value of the coordinate
            :arg y: the y value of the coordinate
            :arg type: int
            :arg type: int
            :returns: true for valid coordiantes, false for invalide coordinates
            :rtype: bool
        """
        return 1 <= x <= self._num_cols and 1 <= y <= self._num_rows
    

