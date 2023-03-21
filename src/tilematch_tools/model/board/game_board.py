"""
    :module_name: game_board
    :module_summary: a classe that represents the board of a tile-matching game
    :module_author: Nathan Mendoza (nathancm@uci.edu)
"""

import logging
from abc import ABC

from ..tiles import Tile, NullTile
from ..exceptions import InvalidBoardPositionError, IllegalBoardContentException

LOGGER = logging.getLogger(__name__)

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
                [ NullTile(**{'position': (x, y),'color':'#D3D3D3'}) for y in range(1, self._num_rows + 1)]
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
        LOGGER.info('Looking at tile located at (%d, %d)', x, y)
        if not self.__board_position_is_valid(x, y):
            LOGGER.error('(%d, %d) is out of bounds', x, y)
            raise InvalidBoardPositionError(
                f"The position ({x}, {y}) is invalid for the given board"
                    )
        return self._board[x - 1][y - 1] # Adjust from cartesian coordinates to valid indices

    def place_tile(self, tile: Tile) -> None:
        """
            place the given tile at its declared position
            :arg tile: tile to place
            :arg type: Tile
            :returns: nothing
            :rtype: None
            :throws InvalidBoardPositionError if the specified position is invalid
            :throws IllegalBoardContentException if the given tile is not a Tile
        """
        if not isinstance(tile, Tile):
            LOGGER.error('Attempted to place a non-tile type on the board')
            raise IllegalBoardContentException(
                    f"tile must be of type Tile, not {type(tile)}"
                    )
        x = tile.position.x
        y = tile.position.y
        if not self.__board_position_is_valid(x, y):
            LOGGER.error('(%d, %d) is out of bounds', x, y)
            raise InvalidBoardPositionError(
                    f"The position ({x}, {y}) is invalid for the given board"
                    )
        if type(tile) == NullTile:
            LOGGER.info('Placing a null tile at (%d, %d) -- skipping availablity checks', x, y)
            self._board[x - 1][y - 1] = tile
            return

        if not self.__board_position_is_available(x, y):
            LOGGER.error('(%d, %d) is already occupied by another tile', x, y)
            raise InvalidBoardPositionError(
                    f"The position ({x}, {y}) is already occupied by another tile"
                    )

        self._board[x - 1][y - 1] = tile
            

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

    def __board_position_is_available(self, x: int, y: int):
        """
            Return true if the given (x, y) ordered pair has no tile in it. False otherwise
            :arg x: the x value of the coordinate
            :arg y: the y value of the coordinate
            :arg type: int
            :arg type: int
            :returns: true for availability, false for unavailability
            :rtype: bool
        """
        return self.__board_position_is_valid(x, y) and type(self._board[x - 1][y - 1]) == NullTile

    def __iter__(self):
        """
            Return a generator that iterate over the board in column-major order
            :rtype: generator
        """
        for x in range(1, self._num_cols + 1):
            for y in range(1, self._num_rows + 1):
                yield self.tile_at(x, y)
