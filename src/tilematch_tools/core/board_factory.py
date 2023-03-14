"""
    :module_name: board_factory
    :module_summary: a class capable of creating new boards of a tile-matching game
    :module_author: Nathan Mendoza (nathancm@uci.edu)
"""

import logging
from abc import ABC
from collections.abc import Iterable

from ..model.board.game_board import GameBoard

LOGGER = logging.getLogger(__name__)

class BoardFactory(ABC):

    @staticmethod 
    def create_board(board_type: GameBoard, width: int, height: int) -> GameBoard:
        """
            Simple factory method for generating a new game board
            :arg board_type: the name of the type of board
            :arg width: the number of columns the board should have
            :arg height: the number of rows the board should have
            :arg type: GameBoard class
            :arg type: int
            :arg type: int
            :return: a new game board object
            :rtype: GameBoard
        """
        LOGGER.info('Board factory churning board of size %sx%s', str(width), str(height))
        return board_type(width, height)

    @staticmethod
    def create_board_with_tiles(board_type: GameBoard, width: int, height: int, tiles: Iterable):
        """
            Factory method that generates a new board, then places the initial tiles provided
            :arg board_type: the board to create
            :arg width: the numer of columns the board should have
            :arg height: the number of rows the board should have
            :arg type: GameBoard class
            :arg type: int
            :arg type: int
            :arg type: iterable
            :returns: the game board state with the initial tiles in place
            :rtype: GameBoard
            :raises: InvalidBoardPosition if not all tiles can be placed
            :raises: IllegalBoardContentError if tiles contains non-tile objects
        """
        the_board = board_type(width, height)
        LOGGER.info('Placing initial set of tiles onto new game board')
        for tile in tiles:
            the_board.place_tile(tile)
            LOGGER.debug('Place the tile at (%d, %d)', tile.position.x, tile.position.y)

        return the_board
