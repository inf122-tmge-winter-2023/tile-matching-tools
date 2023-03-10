"""
    :module_name: board_factory
    :module_summary: a class capable of creating new boards of a tile-matching game
    :module_author: Nathan Mendoza (nathancm@uci.edu)
"""

import logging
from abc import ABC

from ..model.board.game_board import GameBoard

LOGGER = logging.getLogger(__name__)

class BoardFactory(ABC):

    @staticmethod 
    def create_board(board_type: str, width: int, height: int) -> GameBoard:
        """
            Simple factory method for generating a new game board
            :arg board_type: the name of the type of board
            :arg width: the number of columns the board should have
            :arg height: the number of rows the board should have
            :arg type: str
            :arg type: int
            :arg type: int
            :return: a new game board object
            :rtype: GameBoard
        """
        LOGGER.info('Board factory churning board of size %sx%s', str(width), str(height))
        return GameBoard(width, height)